import sys
from pyparsing import *
from icecream import ic

sys.setrecursionlimit(3000)
ParserElement.enablePackrat()
ppc = pyparsing_common
integer = ppc.integer
variable = Word(alphas, exact=1)
operand = integer | variable

undop = Literal("*")
oderop = Literal("+")
notop = Literal("!")

expr = infixNotation(
    operand,
    [
        (notop, 1, opAssoc.RIGHT),
        (undop, 2, opAssoc.LEFT),
        (oderop, 2, opAssoc.LEFT),
    ],
)


class operation():
    
    def _unpack(self,data):
        if isinstance(data,str):
            if len(data) == 1:
                return data
            else:
                raise ValueError
        else:
            return operation(data)

    def __init__(self,data) -> None:
        if isinstance(data,str):
            data=expr.parseString(data.lower().strip()).asList()

        self.operands = []
        self.operator = ""
        if isinstance(data,list):
            if len(data) == 1:
                data = data[0]

        if isinstance(data,list):
            if len(data) == 2:
                self.operator = data[0]
                self.operands.append(self._unpack(data[1]))

            if len(data) >2:
                self.operator = data[1]
                for x in data:
                    if x == self.operator:
                        continue
                    else:
                        self.operands.append(self._unpack(x))
        else:
            raise ValueError


    def __tt(vars):
        if len(vars) == 1:
            yield {vars[0] : False}
            yield {vars[0] : True}
        else:
            for rv in operation.__tt(vars[1:]):
                yield {vars[0] : False, **rv }
                yield {vars[0] : True, **rv }



    def print_tt(self):
        myvars = self.get_vars()
        print(" " + " ".join(myvars)+ "   Y")
        print("--" * len(myvars) + "-----")
        tt=operation.__tt(myvars)
        for line in tt:
            r=[f"{'1' if line[x] else '0'}" for x in line]
            result="1" if self.solve(line) else "0"
            print(" " + " ".join(r) + "   " + result)



    def __repr__(self) -> str:
        if self.operator == "!":
            return f"NICHT {self.operands[0]}"
        else:
            if self.operator == "*":
                return "(" +  " UND ".join([str(x) for x in self.operands]) + ")"

            if self.operator == "+":
                return "(" +  " ODER ".join([str(x) for x in self.operands]) + ")"

    def solve(self,values):
        for vary in self.get_vars():
            if not vary in values:
                raise KeyError
        if self.operator == '!':
            if isinstance(self.operands[0],operation):
                return not self.operands[0].solve(values)
            else:
                return not values[self.operands[0]]

        if self.operator == '*':
            result = True
            for operand in self.operands:
                if isinstance(operand,operation):
                    result = result and operand.solve(values)
                else:
                    result = result and values[operand]
            return result

        if self.operator == '+':
            result = False
            for operand in self.operands:
                if isinstance(operand,operation):
                    result = result or operand.solve(values)
                else:
                    result = result or values[operand]
            return result



    def get_vars(self):
        vars = []
        for x in self.operands:
            if isinstance(x,operation):
                vars += x.get_vars()
            else:
                vars.append(x)
        return list(dict.fromkeys(vars))


    @property
    def hasop(self):
        return len(self.operator)>0
    



test = [
    "(a*b+(a*(!c+b))*c)",
    "a*b+(a*(!c+b)*c)",
    "a *b+ ( a *   ( ! c + (b)  ) *c)",
    "a*b+c+d",
    "a*b+c",
    "!a*!(a+b*!c)",
]

testval={'a':True,'b':False,'c':True, 'd':False}

def tt(vars):
    if len(vars) == 1:
        yield {vars[0] : False}
        yield {vars[0] : True}
    else:
        for rv in tt(vars[1:]):
            yield {vars[0] : False, **rv }
            yield {vars[0] : True, **rv }




for t in test:
    ic(t)
    c=operation(t)
    c.print_tt()


