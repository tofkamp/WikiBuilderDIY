from typing import List

class Statement:
    def __init__(self, lineno):
        self.lineno =lineno

class RightStat(Statement):
    def __init__(self, length: 'Expression', width: 'Expression', lineno: int):
        super().__init__(lineno)
        self.length = length
        self.width = width

class LeftStat(Statement):
    def __init__(self, length: 'Expression', width: 'Expression', lineno: int):
        super().__init__(lineno)
        self.length = length
        self.width = width

class ForwardStat(Statement):
    def __init__(self, length: 'Expression', width: 'Expression', lineno: int):
        super().__init__(lineno)
        self.length = length
        self.width = width

class Instantiate(Statement):
    def __init__(self, name: str, arguments: List['Expression'], lineno: int):
        super().__init__(lineno)
        self.name = name
        self.arguments = arguments
        
# gebruiken we niet
class MoveStat(Statement):
    def __init__(self, xpos: 'Expression', ypos: 'Expression', lineno: int):
        super().__init__(lineno)
        self.xpos = xpos
        self.ypos = ypos

class ConnectorStat(Statement):     # misschien nog male of female of unisex
    def __init__(self, p1x: 'Expression', p1y: 'Expression', p2x: 'Expression', p2y: 'Expression', lineno: int):
        super().__init__(lineno)
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y

class HoleStat(Statement):     # misschien nog male of female of unisex
    def __init__(self,name: str, deltax: 'Expression', deltay: 'Expression', lineno: int):
        super().__init__(lineno)
        self.name = name
        self.deltax = deltax
        self.deltay = deltay

# gebruiken we niet
class RotateStat(Statement):
    def __init__(self, direction: 'Expression', lineno: int):
        super().__init__(lineno)
        self.direction = direction

class Parameter:
    def __init__(self, name: str, lineno: int):
        self.name = name
        self.lineno = lineno

class Definition:
    def __init__(self, name, params: List[Parameter], stats: List[Statement], lineno: int):
        self.name = name
        self.params = params
        self.stats = stats
        self.lineno = lineno


class Expression:
    def __init__(self, lineno):
        self.lineno =lineno

class Subtract(Expression):
    def __init__(self, left: Expression, right: Expression, lineno: int):
        super().__init__(lineno)
        self.left = left
        self.right = right

class Add(Expression):
    def __init__(self, left: Expression, right: Expression, lineno: int):
        super().__init__(lineno)
        self.left = left
        self.right = right

class Multiply(Expression):
    def __init__(self, left: Expression, right: Expression, lineno: int):
        super().__init__(lineno)
        self.left = left
        self.right = right

class Divide(Expression):
    def __init__(self, left: Expression, right: Expression, lineno: int):
        super().__init__(lineno)
        self.left = left
        self.right = right

class Negate(Expression):
    def __init__(self, child: Expression, lineno: int):
        super().__init__(lineno)
        self.child = child

class IntLiteral(Expression):
    def __init__(self, number: int, lineno: int):
        super().__init__(lineno)
        self.number = number

class VariableRef(Expression):
    def __init__(self, name: str, lineno: int):
        super().__init__(lineno)
        self.name = name
