
from ast import Expression, expr


class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        return self.top == None

    def __len__(self): 
        count = 0
        current = self.top
        while current:
            current = current.next
            count += 1
        return count

    def push(self,value):
        newNode = Node(value)
        newNode.next = self.top
        self.top = newNode

     
    def pop(self):
        if self.isEmpty():
            return None
        else:
            temp = self.top
            self.top = self.top.next
            return temp.value

    def peek(self):
        if self.top is None:
            return None
        else:
            return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        try:
            num = float(txt)
            return True
        except:
            return False




    def _getPostfix(self, txt):
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        pemdas = {'(': 0, ')': 0, '^': 3, '*': 2, '/': 2, '+': 1, '-': 1} # Dictionary of characters and their level of precedence
        expression = txt.split()
        postfixString = ''
        # These trackers will keep track of respective characters for checking for invalid inputs
        lparenthesesTrack = 0
        rparenthsesTrack = 0
        operandTrack = 0
        operatorTrack = 0
        for i in range(len(expression)):
            character = expression[i]
            if self._isNumber(character):
                #Converts positive or negative integers into float form
                if len(character) == 1 or len(character) == 2:
                        character = character + '.0'
                # Checks if string is empty for proper spacing
                if postfixString == '':
                    postfixString = postfixString + character
                    operandTrack += 1
                else:
                    postfixString = postfixString + ' ' + character
                    operandTrack += 1
            # If character is any appropriate operator
            elif character in pemdas.keys():
                if character != '(' and character != ')':
                    operatorTrack += 1
                # Checks if character can be pushed into stack no matter what
                if postfixStack.isEmpty() or character == '(':
                    postfixStack.push(character)
                    if character == '(':
                        lparenthesesTrack += 1
                else:
                    if character == ')':
                        rparenthsesTrack += 1
                        if rparenthsesTrack > lparenthesesTrack:
                            return 'Error'
                        # Will pop and push all operators until the left parenthese is on top
                        while postfixStack.peek() != '(':
                            operator = postfixStack.pop()
                            postfixString = postfixString + ' ' + operator
                        # Removes left parenthese
                        postfixStack.pop()
                    # When stack is not empty and the character is not a left parenthese
                    else:
                        # Checks if list is empty first as None cannot be compared to an int
                        # Uses dictioary to compare current operator's precedence to the ones in the stack and pops the ones that
                        # have higher or equal precedence and adds them to string
                        while postfixStack.isEmpty() is not True and pemdas.get(postfixStack.peek()) >= pemdas.get(character):
                            # Adjusts for special case with 2 exponents
                            if character == '^' and postfixStack.peek() == '^':
                                break
                            else:
                                operator = postfixStack.pop()
                                postfixString = postfixString + ' ' + operator
                        postfixStack.push(character) # Pushes operator into stack after
            else: # Returns error if character is not a number or operator in dictionary
                return 'Error'
        # Once all indexing is done will pop and add all remaining operators
        while postfixStack.isEmpty() is not True:
            operator= postfixStack.pop()
            postfixString = postfixString + ' ' + operator
        # Returns an error if the number of operators is not one less than the number of operands
        # This is reltaionship is always true in valid expressions
        if operatorTrack != operandTrack - 1:
            return 'Error'
        # Returns error if number of left and right parentheses are not equal, as that is invalid
        elif lparenthesesTrack != rparenthsesTrack:
            return 'Error'
        return postfixString


    @property
    def calculate(self):
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression

        # YOUR CODE STARTS HERE
        if self.getExpr == 'Error':
            return None
        # Gets postfix expression and makes it a list
        postfixExpr = self._getPostfix(self.getExpr).split()
        for i in range(len(postfixExpr)):
            character = postfixExpr[i]
            # If character is a number than it will be converted to a float and pushed into the stack
            if self._isNumber(character):
                floatNum = float(character)
                calcStack.push(floatNum)
            # If character is an operator than it will pop the 2 top number from the stack
            else:
                firstNum = calcStack.pop()
                secondNum = calcStack.pop()
                # Does the respective operation
                if character == '^':
                    calcStack.push(secondNum ** firstNum)
                elif character == '*':
                    calcStack.push(firstNum * secondNum)
                elif character == '/':
                    calcStack.push(secondNum / firstNum)
                elif character == '+':
                    calcStack.push(firstNum + secondNum)
                elif character == '-':
                    calcStack.push(secondNum - firstNum)
        return calcStack.pop()


#=============================================== Part III ==============================================

class AdvancedCalculator:
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        if word.isalnum() and word[0].isalpha():
            return True
        return False
       

    def _replaceVariables(self, expr):
        expression = expr.split()
        for i in range(len(expression)):
            character = expression[i]
            # Checks if character is a valid variable
            if self._isVariable(character):
                # Replaces variable if it is in dictionary
                if character in self.states.keys():
                    expression.pop(i)
                    expression.insert(i,str(self.states.get(character)))
                else:
                    return None
        return ' '.join(expression)
 
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        progress = {}
        expression = self.expressions.split(';')
        # Indexes all expressions except for last one as it is unique
        for i in range(len(expression) - 1):
            values = expression[i].split('=') # Splits each expression into desired variable and expression/value
            # Checks for invalid variables
            if self._isVariable(values[0].strip()) is False:
                self.states.clear()
                return None
            # Checks if expression was only assigning a number value to a variable and not an expression that has to be solved
            if len(values[1].split()) == 1:
                self.states[values[0].strip()] = float(values[1]) # Updates self.states
                progress[expression[i]] = self.states.copy() # Updates progress with copy of self.states
            else:
                # If any errors arise in these functions it will return None
                # These functions calculate the answer to the expressions
                try:
                    temp = self._replaceVariables(values[1])
                    calcObj.setExpr(temp)
                    answer = calcObj.calculate
                except:
                    return None
                # Returns None if invalid expressions were sent into _getPostfix or calculate but no errors rose
                if answer is None:
                    return None
                self.states[values[0].strip()] = float(answer)
                progress[expression[i]] = self.states.copy()
        end = expression[-1].split() # Splits return statement
        # Determines if return statement is a single variable or equation
        if len(end) == 2:
            progress['_return_'] = self.states.get(end[1])
        # Calculates return expression
        else:
            newList = end[1:] # Gets rid of 'return' so only expression is left in list
            newExpr = ' '.join(newList) 
            temp3 = self._replaceVariables(newExpr)
            calcObj.setExpr(temp3)
            finalAns = calcObj.calculate
            progress['_return_'] = finalAns
        return progress