#import GlobalVars
#import Adventure
#import Player
#from Menu import Menu
#import Character
import inspect
from typing import *


'''
class AdventureBuilder :

    def __init__(self):
        self.vars = {}


    async def Init(self, channel, maker : Player.Player):

        await channel.send("What will be your Adventure's name?")
        name = await GlobalVars.bot.wait_for('message', check= lambda m : m.author.id == maker.author.id)
        channel = name.channel
        await channel.send("What will be your Adventure's description?")
        description = await GlobalVars.bot.wait_for('message', check= lambda m : m.author.id == maker.author.id)
        channel = description.channel
        await channel.send("What will be the minimum party size for your adventure? (0 for no minimum)")
        minPartySize = await GlobalVars.bot.wait_for('message', check= lambda m : m.author.id == maker.author.id and
                                                            m.content.isnumeric() and int(m.content) >= 0)
        channel = minPartySize.channel
        await channel.send("What will be the maximum party size for your adventure? (0 for no minimum)")
        maxPartySize = await GlobalVars.bot.wait_for('message', check= lambda m : m.author.id == maker.author.id and
                                                            m.content.isnumeric() and int(m.content) >= 0)


        self.adventure = Adventure.Adventure(name.content, description.content, int(minPartySize.content), int(maxPartySize.content))
        self.adventure.SetMaker(maker)

    async def Port(self, channel):
        pass


    def FunctionMenus(self):

        self.m_makeAction = Menu('', '', [])
        self.m_makeAction_container = Menu('', '', [])
        self.m_makeAction_statement = Menu('', '', [])
        self.m_makeAction_comment = Menu('', '', [])
        self.m_container_loop = Menu('', '', [])
        self.m_container_condition = Menu('', '', [])
        self.m_loop_for = Menu()
        self.m_loop_while = Menu()

    async def MakeCondition(self):
        pass

    async def MakeStatement(self):
        m_player = Menu()
        m_adventure = Menu()
        m_send = Menu()
        m_input = Menu()

        m_makeStatement = Menu()

    def GetAdventureMemberMenus(self):
        pass

    def GetRoomMemberMenus(self):
        pass

    def GetActionMemberMenus(self):
        pass

    def GetAdventureMethodMenus(self):
        pass

    def GetRoomMethodMenus(self):
        pass

    def GetActionMethodMenus(self):
        pass

'''

def f(a, b, c, d):
    pass

class c:
    v1 = True
    v2 = 13

vars = {'i' : 127,
        's' : "string",
        'b' : True,
        'f' : 3.141,
        'func' : f,
        'c' : c()
        }


exprStr : str = ""
currentObject : object = None

def Expression(varsInScope : Dict[str, object], canPass=True, canIndex=False, canCall=False):

    global exprStr
    global currentObject

    def PrintEasy():
        varsStr = ""
        for v in varsInScope.keys():
            if not(v.startswith('__') and v.endswith('__')):
                varsStr += f"{v}   ({type(varsInScope[v]).__name__})\n"
        varsStr = varsStr[:-1]
        print(varsStr)

    def PrintAdvanced():
        varsStr = ""
        for v in varsInScope.keys():
            if v.startswith('__') and v.endswith('__'):
                varsStr += f"{v}   ({type(varsInScope[v]).__name__})\n"
        print(varsStr)

    def GetVarsInScope(obj):
        d = {}
        for i in dir(obj):
            d[i] = eval(f"obj.{i}")
        return d

    print(exprStr)

    PrintEasy()

    if canCall:
        print('call')
    if canIndex:
        print('index')
    if canPass:
        print('pass')

    while True:
        i = input("> ")

        #if i is a member of
        if i in varsInScope.keys() and i != "expression":
            currentObject = varsInScope[i]
            exprStr += i + "."

            newExprCanCall = '__call__' in dir(varsInScope[i])
            newExprCanIndex = '__getitem__' in dir(varsInScope[i])

            Expression(GetVarsInScope(varsInScope[i]), True, newExprCanIndex, newExprCanCall)
            break

        elif i == 'pass' and canPass:
            # remove the dot at the end
            exprStr = exprStr[:-1]
            print(exprStr)
            break

        elif i == 'call' and canCall:
            # remove the dot at the end
            exprStr = exprStr[:-1]
            exprStr += "("
            for param in inspect.getfullargspec(currentObject).args:
                d = {}
                exprStr += param + "="
                Expression(vars, False)
                exprStr += ", "
            exprStr += ")"
            print('ended func')


        elif i == 'index' and canIndex:
            pass
            break

        elif i == 'expression':
            i = input('expression > ')

            exprStr = exprStr[:-1]
            exprStr += str(eval(i)) + "."

            Expression(GetVarsInScope(eval(i)))
            break

def Decleration(varsInScope : Dict[str, object], canPass=True, canIndex=False, canCall=False):

    global exprStr
    global currentObject

    def PrintEasy():
        varsStr = ""
        for v in varsInScope.keys():
            if not(v.startswith('__') and v.endswith('__')):
                varsStr += f"{v}   ({type(varsInScope[v]).__name__})\n"
        varsStr = varsStr[:-1]
        print(varsStr)

    def PrintAdvanced():
        varsStr = ""
        for v in varsInScope.keys():
            if v.startswith('__') and v.endswith('__'):
                varsStr += f"{v}   ({type(varsInScope[v]).__name__})\n"
        print(varsStr)

    def GetVarsInScope(obj):
        d = {}
        for i in dir(obj):
            d[i] = eval(f"obj.{i}")
        return d

    print(exprStr)

    PrintEasy()

    if canCall:
        print('call')
    if canIndex:
        print('index')
    if canPass:
        print('pass')

    while True:
        i = input("> ")

        #if i is a member of
        if i in varsInScope.keys() and i != "new_var":
            currentObject = varsInScope[i]
            exprStr += i + "."

            newExprCanCall = '__call__' in dir(varsInScope[i])
            newExprCanIndex = '__getitem__' in dir(varsInScope[i])

            Expression(GetVarsInScope(varsInScope[i]), True, newExprCanIndex, newExprCanCall)
            break

        elif i == 'pass' and canPass:
            # remove the dot at the end
            exprStr = exprStr[:-1]
            print(exprStr)
            break

        elif i == 'call' and canCall:
            # remove the dot at the end
            exprStr = exprStr[:-1]
            exprStr += "("
            for param in inspect.getfullargspec(currentObject).args:
                d = {}
                exprStr += param + "="
                Expression(vars, False)
                exprStr += ", "
            exprStr += ")"
            print('ended func')


        elif i == 'index' and canIndex:
            pass
            break

        elif i in varsInScope.keys() and i == 'expression':
            i = input('expression > ')

            exprStr = exprStr[:-1]
            exprStr += str(eval(i)) + "."

            Expression(GetVarsInScope(eval(i)))
            break

        elif i in varsInScope.keys() and i == 'new_variable':
            name = input("var name > ")
            exprStr = name + " = "
            value = Expression(exprvars)
            vars[name] = value


exprvars = vars.copy()
exprvars['expression'] = None
nvvars = vars.copy()
nvvars['new_var'] = None
Decleration(nvvars, False)
