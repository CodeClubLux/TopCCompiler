import AST as Tree
from TopCompiler import Types

def callMethodCode(node, name, type, parser, unary):
    length = 1 if unary else 2
    if type.isType(Types.Interface):
        field = Tree.Field(node)
        field.type = Types.FuncPointer([node.type] * length, node.type)
        field.field = name
        field.addNode(node)
        return field
    else:

        package = "_global" if type.package == "" else type.package
        var = Tree.ReadVar(type.normalName + "_" + name, True, node)
        var.package = package
        var.type = Types.FuncPointer([node.type] * length, node.type)
        return var

def simplifyOperator(operator, iter, parser):
    def overloaded(methodName):
        func = Tree.FuncCall(operator)
        func.addNode(methodName)

        array = []

        for node in operator.nodes:
            func.addNode(node)
            array.append(node.type)

        func.type = operator.type
        operator.owner.nodes[iter] = func

    if operator.type.isType(Types.String):
        func = Tree.FuncCall(operator)

        if operator.kind == "concat":
            func.addNode(Tree.ReadVar("String_op_add", True, parser))
            func.nodes[0].package = "_global"

            for node in operator.nodes:
                if not node.type.isType(Types.String):
                    f = Tree.FuncCall(node)
                    f.type = Types.String(0)
                    f.addNode(callMethodCode(node, "toString", node.type, parser, operator.unary))
                    f.addNode(node)
                    func.addNode(f)
                else:
                    func.addNode(node)

            func.type = operator.type
            operator.owner.nodes[iter] = func
        elif operator.kind == "+":
            overloaded(callMethodCode(operator.nodes[0], "op_add", operator.type, parser, operator.unary))
    elif operator.overload:
        overloaded(callMethodCode(operator.nodes[0], operator.name[operator.name.find("_")+1:], operator.type, parser, operator.unary))

def simplifyAst(parser, ast):

    def simplify(ast, iter):
        for (it, i) in enumerate(ast.nodes):
            simplify(i, it)

        if type(ast) == Tree.Operator:
            simplifyOperator(ast, iter, parser)

    simplify(ast, 0)