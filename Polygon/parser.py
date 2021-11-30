import sys
import os
#https://www.geeksforgeeks.org/getopt-module-in-python/
#https://docs.python.org/3/library/getopt.html
# --library=
# --showimage
# --objpath=
# --help
import getopt

from sly import Lexer, Parser
import ast
from compute import Compute
import Object3d
import ObjectLibrary

class GeoLexer(Lexer):
    tokens = { NUMBER, ID, DEF, END, LEFT, RIGHT, FORWARD,
               PAR_OPEN, PAR_CLOSE, ROTATE, AT, CONNECTOR, HOLE,
               COMMA, SEMI, MUL, DIVIDE, MINUS, PLUS }

    ignore = ' \t'
    ignore_comment = r'\#.*'

    # reconise a float number with or without minus sign
    @_(r'(\d+\.\d+)|(\d+)|(-\d+\.\d+)|(-\d+)')
    def NUMBER(self, t):
        t.value = float(t.value)
        return t
    
    PAR_OPEN = r'\('
    PAR_CLOSE = r'\)'
    MUL = r'\*'
    DIVIDE = '/'
    MINUS = '-'
    PLUS = r'\+'
    COMMA = ','
    SEMI = ';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['def'] = DEF
    ID['end'] = END
    ID['left'] = LEFT
    ID['right'] = RIGHT
    ID['rotate'] = ROTATE
    ID['at'] = AT
    ID['forward'] = FORWARD
    ID['connector'] = CONNECTOR
    ID['hole'] = HOLE

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


class GeoParser(Parser):
    tokens = GeoLexer.tokens

    @_('definition')
    def program(self, p):
        return [p[0]]

    @_('program definition')
    def program(self, p):
        return p[0] + [p[1]]


    @_('DEF ID PAR_OPEN PAR_CLOSE statements END')
    def definition(self, p):
        return ast.Definition(p.ID, [], p.statements, p.lineno)

    @_('DEF ID PAR_OPEN params PAR_CLOSE statements END')
    def definition(self, p):
        return ast.Definition(p.ID, p.params, p.statements, p.lineno)

    @_('param')
    def params(self, p):
        return [p[0]]

    @_('params COMMA param')
    def params(self, p):
        return p[0] + [p[2]]

    @_('ID')
    def param(self, p):
        return ast.Parameter(p.ID, p.lineno)


    @_('statement')
    def statements(self, p):
        return [p[0]]

    @_('statements statement')
    def statements(self, p):
        return p[0] + [p[1]]

    @_('RIGHT expr SEMI')
    def statement(self, p):
        return ast.RightStat(p[1], None, p.lineno)

    @_('RIGHT expr COMMA expr SEMI')
    def statement(self, p):
        return ast.RightStat(p[1], p[3], p.lineno)

    @_('LEFT expr SEMI')
    def statement(self, p):
        return ast.LeftStat(p[1], None, p.lineno)

    @_('LEFT expr COMMA expr SEMI')
    def statement(self, p):
        return ast.LeftStat(p[1], p[3], p.lineno)

    @_('FORWARD expr SEMI')
    def statement(self, p):
        return ast.ForwardStat(p[1], None, p.lineno)

    @_('FORWARD expr COMMA expr SEMI')
    def statement(self, p):
        return ast.ForwardStat(p[1], p[3], p.lineno)

    @_('ROTATE expr SEMI')
    def statement(self, p):
        return ast.RotateStat(p[1], p.lineno)

    # maybe @_('CONNECTOR PAR_OPEN expr COMMA expr PAR_CLOSE PAR_OPEN expr COMMA expr PAR_CLOSE SEMI')
    @_('CONNECTOR expr COMMA expr COMMA expr COMMA expr SEMI')
    def statement(self, p):
        return ast.ConnectorStat(p[1], p[3], p[5], p[7], p.lineno)

    # future
    #@_('HOLE ID PAR_OPEN exprs PAR_CLOSE AT expr COMMA expr SEMI')
    #@_('HOLE ID PAR_OPEN PAR_CLOSE AT expr COMMA expr SEMI')
    @_('HOLE ID AT expr COMMA expr SEMI')
    def statement(self, p):
        return ast.HoleStat(p.ID, p[3], p[5], p.lineno)

    @_('ID PAR_OPEN exprs PAR_CLOSE SEMI')
    def statement(self, p):
        return ast.Instantiate(p.ID, p.exprs, p.lineno)

    @_('ID PAR_OPEN PAR_CLOSE SEMI')
    def statement(self, p):
        return ast.Instantiate(p.ID, [], p.lineno)


    @_('expr')
    def exprs(self, p):
        return [p[0]]

    @_('exprs COMMA expr')
    def exprs(self, p):
        return p[0] + [p[2]]


    @_('addexpr')
    def expr(self, p):
        return p[0]


    @_('mulexpr')
    def addexpr(self, p):
        return p[0]

    @_('addexpr MINUS mulexpr')
    def addexpr(self, p):
        return ast.Subtract(p[0], p[2], p.lineno)

    @_('addexpr PLUS mulexpr')
    def addexpr(self, p):
        return ast.Add(p[0], p[2], p.lineno)


    @_('unary')
    def mulexpr(self, p):
        return p[0]

    @_('mulexpr MUL unary')
    def mulexpr(self, p):
        return ast.Multiply(p[0], p[2], p.lineno)

    @_('mulexpr DIVIDE unary')
    def mulexpr(self, p):
        return ast.Divide(p[0], p[2], p.lineno)


    @_('minuses term')
    def unary(self, p):
        invert, lineno = p[0]
        if lineno is None or not invert:
            return p[1]
        return ast.Negate(p[1], lineno)

    @_('')
    def minuses(self, p):
        return False, None

    @_('minuses MINUS')
    def minuses(self, p):
        invert, lineno = p[0]
        if lineno is None:
            lineno = p.lineno

        return not invert, lineno


    @_('NUMBER')
    def term(self, p):
        return ast.IntLiteral(p.NUMBER, p.lineno)

    @_('ID')
    def term(self, p):
        return ast.VariableRef(p.ID, p.lineno)

    @_('PAR_OPEN expr PAR_CLOSE')
    def term(self, p):
        return p[1]

    def error(self, p):
        if p:
            print("Syntax error at token", p.type,"at line",p.lineno)
            # Just discard the token and tell the parser it's okay.
            self.errok()
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    
    # --library=
    # --showimage
    # --objpath=
    # --help
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hilo:", ["help", "library=","showimage","objpath="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print(opts)
        print(args)
        #usage()
        sys.exit(2)
    libraryfilename = None
    objpath = None
    showimage = False
    
    for o, a in opts:
        if o in ("--showimage", "-i"):
            showimage = True
        elif o in ("-h", "--help"):
            #usage()
            sys.exit()
        elif o in ("-l", "--library"):
            libraryfilename = a
        elif o in ("-o", "--objpath"):
            objpath = a
        else:
            assert False, "unhandled option"
    if len(args) == 0:
        print("Missing input file!")
        sys.exit(1)
    
    lib = ObjectLibrary.ObjectLibrary()
    if libraryfilename:
        if os.path.exists(libraryfilename):
            #print("load library",libraryfilename)
            lib.load(libraryfilename)
        
    for inputfilename in args:
        pathname,basenameext = os.path.split(inputfilename)
        basename,ext = os.path.splitext(basenameext)
        lexer = GeoLexer()
        parser = GeoParser()

        #with open("library/whalm/" + inputfilename + ".geo") as handle:
        with open(inputfilename) as handle:
            text = handle.read()
        # debug tokens
        #x = lexer.tokenize(text)
        #for tok in x:
        #    print("Token",tok)
        
        defis = parser.parse(lexer.tokenize(text))
        # debug definitions
        #print("Definitions:")
        #for defi in defis:
        #    print(f"  - {defi.name}")
        #if not defis:
        #    print(f"  None!")

        #print()
        #print("Executing 'main':")
        c = Compute(defis)
        obj2d = c.run()
        obj3d = Object3d.Object3d(basename)

        if showimage:
            obj2d.show_image()
        
        # create 3d object from shape in 2d object
        obj3d.from_Object2d(obj2d)
        #for c in obj3d.connectors2:
        #        print(c.widthX,c.heightY,c.depthZ)
        #obj3.rotate(90,90,0)   # put it down on the ground

        if objpath:
            # write obj file with the name of the inputfile
            obj3d.export2obj(objpath + "/" + basename,scale = 1000)
            #c.img.crop(c.img.getbbox()).save("a.png")

        # add/update shape into the library
        lib.add_object(obj3d)
    if libraryfilename:
        lib.save(libraryfilename)
    #lib.save("Library/whalm.json")
