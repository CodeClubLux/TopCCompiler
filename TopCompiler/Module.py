#This module enables loading plugins

from TopCompiler import Lexer
from TopCompiler import Parser
from TopCompiler import TypeInference

import importlib

def nothing():
    pass

def addKeyword(keyword, parse, type=nothing):
    Lexer.keywords.append(keyword)
    Parser.exprToken[keyword] = parse
    if type != nothing:
        TypeInference.checkTyp.append(type)

def indexOfInRules(rules,searchingFor):
    for (i, (typ,reg)) in enumerate(rules):
        if typ == searchingFor:
            return i

def addLexRule(rule, before=False):
    if not before:
        Lexer.token_specification.append(rule)
    else:
        rules = Lexer.token_specification
        rules.insert(indexOfInRules(rules,before), rule)

def addRule(rule, parse, type=nothing, before=False):
    addLexRule(rule, before)

    Parser.exprType[rule[0]] = parse
    if type != nothing:
        TypeInference.checkTyp[rule] = type

def removeRule(rule):
    rules = Lexer.token_specification
    if rule in TypeInference.checkTyp:
        del TypeInference.checkTyp[rule]
    if rule in Parser.exprType:
        del Parser.exprType[rule]
    try:
        del rules[indexOfInRules(rules,rule)]
    except TypeError:
        pass

def removeKeyword(rule):
    rules = Lexer.token_specification
    if rule in TypeInference.checkTyp:
        del TypeInference.checkTyp[rule]
    if rule in Parser.exprToken:
        del Parser.exprToken[rule]
        Lexer.token_specification = rules[:Lexer.normalLength]

import importlib.util
import os
from TopCompiler import Error

transforms = {}

def importModule(path):
    moduleName = os.path.basename(os.path.splitext(path)[0])
    spec = importlib.util.spec_from_file_location(moduleName, path)
    if not spec:
        Error.error("Cannot load transform from path "+path)

    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    transforms[moduleName] = foo

def initModule(moduleName):
    try:
        transforms[moduleName].init()
    except Exception as e:
        Error.error("Error "+str(e)+" happened when intializing syntax extension "+moduleName)

def removeModule(moduleName):
    try:
        transforms[moduleName].remove()
    except Exception as e:
        Error.error("Error "+str(e)+" happened when removing syntax extension "+moduleName)

shouldCallTyp = {}
shouldCallToken = {}
def typShouldCall(typ, should):
    shouldCallTyp[typ] = should

def tokenShouldCall(token, should):
    shouldCallToken[token] = should

def shouldCall(token):
    try:
        return shouldCallToken[token.token]
    except KeyError:
        try:
            return shouldCallTyp[token.type]
        except KeyError:
            return True