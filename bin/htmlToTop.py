from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.output = []
        self.indent = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            tag = "link"

        self.output.append(self.indent + tag + " [")
        indent = self.indent
        if len(attrs) > 1:
            self.output.append("\n")
            self.indent += " " * 4

        for (key, value) in attrs:
            if not value:
                value = "true"
            if key in ["type", "async", "float", "defer"]:
                key = "_" + key

            if not value in "true":
                value = '"' + value + '"'

            if len(attrs) > 1:
                self.output.append(self.indent)
            self.output.append(key + " " + value)
            if len(attrs) > 1:
                self.output.append("\n")

        if len(attrs) > 1:
            self.output.append(indent)
        self.output.append("], [\n")
        self.indent = indent + " " * 4

    def handle_endtag(self, tag):
        self.indent = self.indent[:-4]
        self.output.append(self.indent + "]\n")

    def handle_data(self, data):
        regex = r"[ ]{2,}"
        data = re.sub(regex, "", data).replace("\n", "")
        if data != "":
            self.output.append(self.indent + '"' + data + '"\n')

    def getCode(self):
        return "".join(self.output)

html = """
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/CompilerLuke" data-size="large" data-show-count="true" aria-label="Follow @CompilerLuke on GitHub">Follow @CompilerLuke</a>
"""

parser = MyHTMLParser()
parser.feed(html)

print(html)
print("====")
print(parser.getCode())