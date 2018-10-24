'''
    This program manages a list of complex numbers (given in the form A+Bi) and has the following features:
        -> add <number> = adds the number at the end of the list
        -> insert <number> at <position> = inserts the number at the given position based on zero-indexing
        -> remove <position> = removes the number at the given position
        -> remove <start position> to <ending position> = removes the numbers which positions are in the given interval
        -> replace <old number> with <new number> = replaces all the occurences of the old number with the new given number
        -> list = writes the list of numbers
        -> list real <start position> to <end position> = lists all the real numbers between given positions
        -> list modulo [< | = | >] <number> = lists all numbers which have the absolute value < / = / > than the given number
        ---------------- iteration 1 stops here ----------------
        -> sum <start position> to <end position> = writes the sum of the numbers between the given positions in the list
        -> product <start position> to <end position> = writes the product of the numbers between the given positions
        -> filter real = keeps only the real numbers in the list
        -> filter modulo [< | = | >] <number> = keeps only the numbers which absolute value satisfy the given condition
        -> undo = the last operation that has modified program data will be reversed
'''

def printUserOptions():
    print("There are several operations you could do to the list:")
    print("add <number> = adds a complex number (in form A+Bi) at the end of the list")
    print("insert <number> at <position> = inserts the complex number (in form A+Bi) at the given position (positions begin from 0)")
    print("remove <position> = removes the number at the given position")
    print("remove <start position> to <ending position> = removes the numbers which positions are in the given interval")
    print("replace <old number> with <new number> = replaces all the occurences of the old number with the new given number (both must be complex in the form A+Bi!)")
    print("list = writes the list of numbers")
    print("list real <start position> to <end position> = lists all the real numbers between given positions")
    print("list modulo [< | = | >] <integer number> = keeps in the list only the numbers which absolute value satisfy the given condition")
    print("exit = exits the application")
    '''
        print("sum <start position> to <end position> = writes the sum of the numbers between the given positions in the list")
        print("product <start position> to <end position> = writes the product of the numbers between the given positions in the list")
        print("filter real = keeps only the real numbers in the list")
        print("filter modulo [< | = | >] <number> = keeps only the numbers which absolute value satisfy the given condition")
        print("undo = the last operation that has modified program data will be reversed")
    '''


def stringContainsCommand(choiceString, choiceCommand):
    '''
        This function should tell if the command 'choiceCommand' is found in 'choiceString'
        :param choiceString: string - the string in which we need to search for the specific command
        :param choiceCommand: string - the string which need to be searched
        :return: True or False, based by the search result
    '''
    if choiceString.find(choiceCommand) == 0: # the string begins with the given command
        return True
    return False


def countForeignCharacters(complexNumberString, separators):
    '''
        This function counts the foreign characters in a string (all characters which are not in the separator string
        or are not digits)
        :param complexNumberString: string which must be validated as a complex number
        :param separators: string which contains the valid non-digit characters
        :return: int - number of such foreign characters
    '''
    # returning the length of a particular list which encapsulates all the characters which are not digits and not included in the separators string
    foreignCharactersCounter = len([foreignCharacter for foreignCharacter in complexNumberString if foreignCharacter.isdigit() == False and foreignCharacter not in separators])
    return foreignCharactersCounter


def countSigns(complexNumberString):
    '''
        This function counts the arithmetic signs in a string which must be validates as a complex number
        :param complexNumberString: string which must be validated as a complex number
        :return: int - number of arithmetic signs
    '''
    # returning the length of a particular list which encapsulates all the characters which are either '+' or '-'
    signsCounter = len([sign for sign in complexNumberString if sign in "+-"])
    return signsCounter


def countDigits(complexNumberString):
    '''
        This function counts the digits present in the complex number string which should be evaluated
        :param complexNumberString: string which should be evaluated if it represents a valid complex number representation
        :return: int - the number of digits present in the string
    '''
    # returning the length of a particular list which encapsulates all the digits in the provided string
    return len([digit for digit in complexNumberString if digit.isdigit() == True])


def extractIfValidComplexNumber(complexNumberString):
    '''
        This function tests if a given string represents a valid complex number in form A+Bi
        :param complexNumberString: string - should be tested if it represents a valid complex number (in form A+Bi)
        :return: True, real part, imaginary part (if the number is valid)
                 False, 0, 0 if the number is not valid
    '''
    complexNumberString = complexNumberString.lstrip()  # erasing the unnecessary leading spaces
    realPartSign = imaginaryPartSign = 0  # they tell if the real (imaginary) part are either positive or negative (-1 for negative, 1 for positive)
    realPart = imaginaryPart = 0  # the real and the imaginary part - integers
    justPutSign = False  # flag for signaling patterns with 2 consecutive signs
    beganProcessingImaginaryPart = False
    foundDigitsInRealPart = foundDigitsInImaginaryPart = False  # for signaling if the real part or the imaginary part has any digits
    foundImaginaryUnit = False  # flag to avoid multiple i's
    separators = "+-i"

    if countForeignCharacters(complexNumberString, separators) > 0:  # no foreign characters allowed
        return False, 0, 0
    if countSigns(complexNumberString) > 2:  # if the string has 3 or more signs then it isn't valid
        return False, 0, 0

    if complexNumberString[0] in "+-":
        startingPosition = 1  # skip the sign
        justPutSign = True
        if (complexNumberString[0] == '+'):
            realPartSign = 1
        else:
            realPartSign = -1
    else:
        realPartSign = 1  # if there isn't any sign at the beginning of the string
        startingPosition = 0  # there must be digits

    for i in range(startingPosition, len(complexNumberString)):
        character = complexNumberString[i]
        if character.isdigit() == True:
            if foundImaginaryUnit == True:  # no digits should be found after i
                return False, 0, 0
            justPutSign = False
            if beganProcessingImaginaryPart == False:
                foundDigitsInRealPart = True
                realPart = realPart * 10 + int(character)  # appending the digit to the current real part
            else:
                foundDigitsInImaginaryPart = True
                imaginaryPart = imaginaryPart * 10 + int(character)  # appending the digit to the current real part
        elif character in "+-":
            if justPutSign == True:  # no signs must be one next to another (e.g. 1+-i or +-3)
                return False
            if character == '+':
                if realPartSign == 0:
                    realPartSign = 1
                else:
                    beganProcessingImaginaryPart = True
                    imaginaryPartSign = 1
            else:
                if realPartSign == 0:
                    realPartSign = -1
                else:
                    beganProcessingImaginaryPart = True
                    imaginaryPartSign = -1
        else:
            if foundImaginaryUnit == True:  # there shouldn't be more than one 'i' character in a complex number represented as a string
                return False, 0, 0
            foundImaginaryUnit = True

    if countDigits(complexNumberString) == 0 and foundImaginaryUnit == False:
        return False, 0, 0

    if foundImaginaryUnit == False and beganProcessingImaginaryPart == True:  # addition between two numbers (e.g. 3+5, 4+2+1 etc.)
        return False, 0, 0

    if foundImaginaryUnit == True and beganProcessingImaginaryPart == False:  # having only an imaginary part
        # the real part is missing so the real part is actually the imaginary part
        foundDigitsInImaginaryPart = foundDigitsInRealPart
        imaginaryPart = realPart
        realPart = 0

        imaginaryPartSign = realPartSign
        realPartSign = 1

    if imaginaryPart == 0 and foundImaginaryUnit == True and foundDigitsInImaginaryPart == False:
        imaginaryPart = 1

    return True, realPart * realPartSign, imaginaryPart * imaginaryPartSign


def appendToList(complexNumberList, complexNumber):
    '''
        :param complexNumberList: list which encapsulates all the complex numbers
        :param complexNumber: tuple which represents (A, B) in a valid complex number in form A+Bi
        :return: nothing
    '''
    complexNumberList.append(complexNumber)


def updateCommandsHistory(undoHistory, complexNumberList):
    '''

        :param undoHistory: list of dictionaries - contains all the intermediate phases of the complex number list
        :param complexNumberList: the list representing the state of the complex number list before affecting it
        :return: nothing
    '''
    undoHistory.append(complexNumberList)


def checkChoiceStringForBadCharacters(choiceString):
    '''
        This function will check if the provided string consists only of alphanumeric and '+' or '-' characters
        :param choiceString: string - provided by the user
        :return: True if the provided string consists only of alphanumeric and '+' or '-' characters
                 False if contrary
    '''
    # if there are any characters which are not alphanumeric or +, - or space then it's considered a forbidden character
    return len([character for character in choiceString if (not character.isalnum()) and (character not in "+- ")]) == 0


def getComplexNumber(complexNumberList, position):
    '''
        This function returns the complex number in the list at a certain position
        :param complexNumberList: list of complex numbers
        :param position: int - index
        :return: the tuple present in that index
        :except: may throw a KeyError exception when the key is not found in the list
    '''
    return complexNumberList[position]


def getRealPart(complexNumber):
    '''
        This function returns the real part of a valid complex number
        :param complexNumber: a valid complex number (a tuple in form (A, B) from the valid complex number form A+Bi)
        :return: int - the real part of the complex number
    '''
    return complexNumber[0]


def getImaginaryPart(complexNumber):
    '''
        This function returns the imaginary part of a valid complex number
        :param complexNumber: a valid complex number (a tuple in form (A, B) from the valid complex number form A+Bi)
        :return: int - the imaginary part of the complex number
    '''
    return complexNumber[1]


def createComplexNumber(realPart, imaginaryPart):
    '''
        This function creates a complex number tuple by having the real part and the complex part
        :param realPart: int - the real part of a complex number
        :param imaginaryPart: int - the imaginary part of a complex number
        :return: (realPart, imaginaryPart) - a tuple which represents the new complex number
    '''
    return (realPart, imaginaryPart)


def addComplexNumberToList(complexNumberList, choiceString, undoHistory):
    '''
        This function should prepare a complex number to be added in the list and add it
        :param complexNumberList: list which encapsulates all the complex numbers
        :param choiceString: string - user's choice
        :param undoHistory: list of dictionaries - contains all the intermediate phases of the complex number list
        :return: nothing
    '''
    if checkChoiceStringForBadCharacters(choiceString) == False:
        raise ValueError(r"use of the command 'add'")
    choiceString, complexNumberString = choiceString.split(" ")
    isValid, realPart, imaginaryPart = extractIfValidComplexNumber(complexNumberString)
    if isValid == False:
        raise ValueError("provided complex number")
    complexNumber = createComplexNumber(realPart, imaginaryPart)
    updateCommandsHistory(undoHistory, complexNumberList)
    appendToList(complexNumberList, complexNumber)


def setComplexNumber(complexNumberList, complexNumber, position):
    '''
        This function inserts a valid complex number on a certain position
        :param complexNumberList: list of complex numbers (tuples)
        :param complexNumber: tuple (A, B) in form of A+Bi, representing a valid complex number
        :param position: int - position
        :return: nothing
    '''
    if position < len(complexNumberList) and position >= 0:  # position in [0, n) where n is the length of the list
        complexNumberList.insert(position, complexNumber)
    elif position >= len(complexNumberList):  # position in [n, oo)
        appendToList(complexNumberList, complexNumber)
        print("The given position was out of the list's range so the number was added at the end of the list.")
    elif position < 0:  # position in (-oo, 0)
        complexNumberList.insert(0, complexNumber)
        print("The given position was out of the list's range so the number was added at the beginning of the list.")


def insertComplexNumberToList(complexNumberList, choiceString, undoHistory):
    '''
        This function should evaluate a choice string in order to insert a complex number on a certain position
        :param complexNumberList: a list of complex numbers (tuples)
        :param choiceString: string - the string the user entered
        :param undoHistory: the history of the list evolution
        :return: nothing
    '''
    if checkChoiceStringForBadCharacters(choiceString) == False:
        raise ValueError(r"use of the command 'insert'")
    choiceString, complexNumberString, atString, position = choiceString.split(" ")
    if atString != "at":
        raise ValueError(r"use of the command 'insert'")
    isValid, realPart, imaginaryPart = extractIfValidComplexNumber(complexNumberString)
    if isValid == False:
        raise ValueError("provided complex number")
    complexNumber = createComplexNumber(realPart, imaginaryPart)
    updateCommandsHistory(undoHistory, complexNumberList)
    try:
        position = int(position)
    except ValueError:
        print("Invalid provided position, please reintroduce your command.")
    setComplexNumber(complexNumberList, complexNumber, position)


def printComplexNumbersList(complexNumberList):
    if complexNumberList == []:
        print("The set is empty!")
    else:
        for complexNumber in complexNumberList:
            realPart = getRealPart(complexNumber)
            imaginaryPart = getImaginaryPart(complexNumber)
            if (realPart != 0 or (realPart == 0 and imaginaryPart == 0)):
                answerString = str(realPart)
            else:
                answerString = ""
            if imaginaryPart > 0:
                if imaginaryPart != 1:
                    answerString += "+" + str(imaginaryPart) + "i"
                else:
                    answerString += "+i"
            elif imaginaryPart < 0:
                if imaginaryPart != -1:
                    answerString += str(imaginaryPart) + "i"
                else:
                    answerString += "-i"
            print(answerString)


def removeComplexNumberFromPosition(complexNumberList, position):
    '''
        This function removes an element from a certain position in a complex number list
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param position: int - position of the element to be removed
        :return: nothing
        :except: might throw a ValueError exception
    '''
    if position >= 0 and position < len(complexNumberList):
        del complexNumberList[position]
    else:
        print("Cannot remove a non-existing element! Please reintroduce your command.")


def removeComplexNumbersInterval(complexNumberList, startPosition, endPosition):
    '''
        This function should remove the complex numbers with indices between startPosition and endPosition
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param startPosition: starting position for removal
        :param endPosition: ending position for removal
        :return: nothing
    '''
    startPosition = int(startPosition)
    endPosition = int(endPosition)
    if endPosition < startPosition:  # incorrect interval
        raise ValueError("provided interval")
    startPosition = max(startPosition, 0)  # force the interval to begin either with the startPosition or with 0
    endPosition = min(endPosition, len(complexNumberList) - 1)
    while startPosition >= 0 and startPosition < len(complexNumberList) and endPosition >= startPosition:
        endPosition -= 1
        del complexNumberList[startPosition]


def getNumberOfWords(choiceString):
    auxiliaryString = choiceString  # using an auxiliary string to decide which syntax to use for the remove command
    splitResult = auxiliaryString.split(" ")
    return len(splitResult)


def removeComplexNumbersFromList(complexNumberList, choiceString, undoHistory):
    '''
        This function should evaluate a choice string in order to remove a complex number(s) from certain position(s)
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param choiceString: string - user's input
        :param undoHistory: list of previous lists
        :return: nothing
    '''
    if checkChoiceStringForBadCharacters(choiceString) == False:
        raise ValueError(r"use of the command 'remove'")
    numberOfWords = getNumberOfWords(choiceString)  # calculating the number of words
    if numberOfWords == 2:  # remove <position> scenario
        choiceString, position = choiceString.split(" ")
        try:
            position = int(position)
        except ValueError:
            print("Invalid provided position, please reintroduce your command.")
        updateCommandsHistory(undoHistory, complexNumberList)
        removeComplexNumberFromPosition(complexNumberList, position)
    elif numberOfWords == 4:  # remove <start> to <stop>
        choiceString, startPosition, toString, endPosition = choiceString.split(" ")
        if toString != "to":
            raise ValueError(r"use of the command 'remove'")
        updateCommandsHistory(undoHistory, complexNumberList)
        removeComplexNumbersInterval(complexNumberList, startPosition, endPosition)
    else:
        raise ValueError(r"use of the command 'remove'")


def replaceComplexNumbersInList(complexNumberList, oldComplexNumber, newComplexNumber):
    '''
        This function replaces all occurences of the valid complex number 'oldComplexNumber' with 'newComplexNumber'
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param oldComplexNumber: tuple - valid complex number which needs to be replaces
        :param newComplexNumber: tuple - valid complex number which consists the object of replacement
        :return: nothing
    '''
    for i in range(len(complexNumberList)):
        if complexNumberList[i] == oldComplexNumber:
            complexNumberList[i] = newComplexNumber


def replaceComplexNumbersFromList(complexNumberList, choiceString, undoHistory):
    '''
        This function evaluates a choice string in order to replace a valid complex number with another valid complex
        number
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param choiceString: string - user's input
        :param undoHistory: list of previous lists
        :return: nothing
    '''
    choiceString, oldComplexNumberString, withString, newComplexNumberString = choiceString.split(" ")
    if withString != "with":
        raise ValueError(r"use of the command 'replace'")
    isOldValid, oldRealPart, oldImaginaryPart = extractIfValidComplexNumber(oldComplexNumberString)
    isNewValid, newRealPart, newImaginaryPart = extractIfValidComplexNumber(newComplexNumberString)

    if isOldValid == False or isNewValid == False:
        raise ValueError("provided complex number(s)")
    oldComplexNumber = createComplexNumber(oldRealPart, oldImaginaryPart)
    newComplexNumber = createComplexNumber(newRealPart, newImaginaryPart)
    updateCommandsHistory(undoHistory, complexNumberList)
    replaceComplexNumbersInList(complexNumberList, oldComplexNumber, newComplexNumber)


def getPositionsListReal(choiceString, listLength):
    '''
        This function extracts the starting and the ending position from a valid 'list real <startPosition> to <endPosition>'
        :param choiceString: string - a syntactically valid string for the 'list real <start position> to <end position>' request
        :param listLength: the used list's length
        :return: 2 integers representing the starting and the ending position from the user's provided string
        :except: might throw ValueError for non-integers as the starting and ending position
                                        for the situation when startPosition > endPosition
                                        for the situation when startPosition < 0
                                        for the situation when endPosition < n (where n = the list's length)
    '''
    choiceString, realString, startingPosition, toString, endingPosition = choiceString.split(" ")
    startingPosition = int(startingPosition)
    endingPosition = int(endingPosition)
    if startingPosition > endingPosition:  # invalid interval
        raise ValueError("provided interval")
    if startingPosition < 0:  # beginning position is below 0
        startingPosition = 0
    if endingPosition >= listLength:  # ending position is out of the array
        endingPosition = listLength - 1
    return startingPosition, endingPosition


def getListRealNumbersInInterval(complexNumberList, choiceString, listLength):
    '''
        This function lists the real numbers within a certain interval as entered by the user
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param choiceString: a valid request of listing the real numbers between certain positions
        :param listLength: the length of the used list
        :return: the list of the real numbers between the certain positions
    '''
    startingPosition, endingPosition = getPositionsListReal(choiceString, listLength)
    return [complexNumberList[i] for i in range(startingPosition, endingPosition + 1) if getImaginaryPart(complexNumberList[i]) == 0]


def validListRealCommand(choiceString):
    '''
        This function tells whether the string provided by the user is a valid 'list real <start position> to <end position>' request
        :param choiceString: string - needs to be validated as a valid 'list real <start position> to <end position>' request
        :return: True or False
    '''
    choiceString, realString, startPos, toString, endPos = choiceString.split(" ")
    if realString != "real":
        return False
    if toString != "to":
        return False
    try:
        startPos = int(startPos)
        endPos = int(endPos)
    except:
        return False
    return True


def validListModuloCommand(choiceString):
    '''
        This function tells whether the string provided by the user is a valid 'list modulo [< / = / >] <number>' request
        :param choiceString: string - needs to be validated as a valid 'list modulo [< / = / >] <number>' request
        :return: True or False
    '''
    choiceString, moduloString, signString, numberString = choiceString.split(" ")
    if moduloString != "modulo":
        return False
    if len(signString) != 1 or signString not in "<=>":
        return False
    try:
        numberString = float(numberString)
    except:
        return False
    return True

def getSquaredAbsoluteValue(complexNumber):
    '''
        This function computes the square of the absolute value of the complex number
        It is more appropriate to compare squares than to compute floating-point numbers efficience-wise and simplicity-wise
        :param complexNumber: tuple - (A, B) representing a valid complex number in the form A+Bi
        :return:
    '''
    realPart = getRealPart(complexNumber)
    imaginaryPart = getImaginaryPart(complexNumber)
    return realPart ** 2 + imaginaryPart ** 2

def compareAbsoluteValue(complexNumber, signString, targetValue):
    '''
        This function compares a complex number's absoluteValue to a certain target value according to the provided sign
        :param complexNumber: tuple - (A, B) representing a valid complex number in the form A+Bi
        :param signString: string (represents a single character) - in the set "<=>"
        :param targetValue: float - the value the complex number's absolute value must be compared with
        :return: True or False according to the truth value of the given relation
    '''
    squaredComplexNumberAbsoluteValue = getSquaredAbsoluteValue(complexNumber)
    if signString == '=':
        return squaredComplexNumberAbsoluteValue == targetValue * targetValue
    elif signString == '<':
        if targetValue < 0:
            return False
        return squaredComplexNumberAbsoluteValue < targetValue * targetValue
    else:
        if targetValue < 0:
            return True
        return squaredComplexNumberAbsoluteValue > targetValue * targetValue


def getListModuloNumbers(complexNumberList, choiceString):
    '''
    This function returns the list of all the numbers which satisfy the given string condition regarding their absolute value
    :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
    :param choiceString: a valid 'list modulo [< / = / >] <number>' request
    :return: the list of numbers for which the given relation is true
    '''
    choiceString, moduloString, signString, absoluteValue = choiceString.split(" ")
    try:
        absoluteValue = float(absoluteValue)
    except ValueError:
        print("Invalid provided absolute value, please reintroduce your command.")

    return [complexNumber for complexNumber in complexNumberList if compareAbsoluteValue(complexNumber, signString, absoluteValue) == True]


def listComplexNumbersFromList(complexNumberList, choiceString):
    '''
        This function evaluates a choice string provided by the user and if it is valid, it provides list features as stated
        in the description of the program
        :param complexNumberList: list of tuples which represent valid complex numbers (A, B) in the form A+Bi
        :param choiceString: string - user's input
        :except: might raise ValueError for invalid user input
        :return: nothing
    '''
    listLength = len(complexNumberList)
    if choiceString == "list":
        printComplexNumbersList(complexNumberList)
    else:
        numberOfWords = getNumberOfWords(choiceString)
        if numberOfWords == 5:  # list real <start> to <stop>
            if validListRealCommand(choiceString):
                printComplexNumbersList(getListRealNumbersInInterval(complexNumberList, choiceString, listLength))
            else:
                raise ValueError(r"use of the command 'list'")
        elif numberOfWords == 4:  # list modulo [<=>] number
            if validListModuloCommand(choiceString):
                printComplexNumbersList(getListModuloNumbers(complexNumberList, choiceString))
            else:
                raise ValueError(r"use of the command 'list'")
        else:
            raise ValueError(r"use of the command 'list'")

def handleRaisedValueError(valueError):
    '''
    This function handles the raised error in case of a faulty use by the user by notifying the user about their mistake.
    :param valueError: string - error string extracted from a thrown ValueError
    :return:
    '''
    errorString = "Invalid " + valueError + ", please reintroduce your command."
    print(errorString)


def runCommandBasedApplication():
    complexNumberList = [(-1, 0), (2, -3), (4, -5), (-10, 1), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]  # the list of complex numbers
    undoHistory = []  # the list history
    choiceString = ""  # user's entered choice

    printUserOptions()

    while choiceString != "exit":
        choiceString = input(">")
        choiceString = choiceString.lstrip()  # erasing any unnecessary leading spaces
        try:
            if stringContainsCommand(choiceString, "add"):
                addComplexNumberToList(complexNumberList, choiceString, undoHistory)
            elif stringContainsCommand(choiceString, "insert"):
                insertComplexNumberToList(complexNumberList, choiceString, undoHistory)
            elif stringContainsCommand(choiceString, "remove"):
                removeComplexNumbersFromList(complexNumberList, choiceString, undoHistory)
            elif stringContainsCommand(choiceString, "replace"):
                replaceComplexNumbersFromList(complexNumberList, choiceString, undoHistory)
            elif stringContainsCommand(choiceString, "list"):
                listComplexNumbersFromList(complexNumberList, choiceString)
            elif choiceString != "exit":
                print("Invalid command, please try again.")
        except ValueError as valueError:
            valueError = str(valueError)
            handleRaisedValueError(valueError)
        except IndexError:
            print("Invalid data provided, please reintroduce your command.")


def testExtractComplexNumber():
    assert extractIfValidComplexNumber("1+i") == (True, 1, 1)
    assert extractIfValidComplexNumber("5i") == (True, 0, 5)
    assert extractIfValidComplexNumber("-5i") == (True, 0, -5)
    assert extractIfValidComplexNumber("-+4+5") == (False, 0, 0)
    assert extractIfValidComplexNumber("5i+4") == (False, 0, 0)
    assert extractIfValidComplexNumber("-i") == (True, 0, -1)
    assert extractIfValidComplexNumber("4+5") == (False, 0, 0)
    assert extractIfValidComplexNumber("+5 22i") == (False, 0, 0)
    assert extractIfValidComplexNumber("i-i") == (False, 0, 0)
    assert extractIfValidComplexNumber("4i-4i") == (False, 0, 0)
    assert extractIfValidComplexNumber("0-0i") == (True, 0, 0)
    assert extractIfValidComplexNumber("-0i") == (True, 0, 0)
    assert extractIfValidComplexNumber("0") == (True, 0, 0)
    assert extractIfValidComplexNumber("-0") == (True, 0, 0)
    assert extractIfValidComplexNumber("+") == (False, 0, 0)
    assert extractIfValidComplexNumber("+0") == (True, 0, 0)
    assert extractIfValidComplexNumber("i-0") == (False, 0, 0)


def testAppendToList():
    list = []
    appendToList(list, (0, 0))
    assert list == [(0, 0)]
    appendToList(list, (-1, -3))
    assert list == [(0, 0), (-1, -3)]


def testInsertToList():
    list = []
    undo = []
    insertComplexNumberToList(list, "insert 3+5i at 0", undo)
    assert list == [(3, 5)]
    insertComplexNumberToList(list, "insert i at 0", undo)
    assert list == [(0, 1), (3, 5)]
    insertComplexNumberToList(list, "insert -i at -1", undo)
    assert list == [(0, -1), (0, 1), (3, 5)]


def testRemoveSingleElement():
    list = [(-1, 0), (2, -3), (4, -5), (-10, 1), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    removeComplexNumberFromPosition(list, 2)
    assert list == [(-1, 0), (2, -3), (-10, 1), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    removeComplexNumberFromPosition(list, 3)
    assert list == [(-1, 0), (2, -3), (-10, 1), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    #removeComplexNumberFromPosition(list, 1000)  # should throw value error - checked!


def testRemoveMultipleElements():
    list = [(-1, 0), (2, -3), (4, -5), (-10, 1), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    removeComplexNumbersInterval(list, 0, 3)
    assert list == [(1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    removeComplexNumbersInterval(list, 100, 200)
    assert list == [(1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]


def testReplace():
    list = [(-1, 0), (2, -3), (4, -5), (-1, 0), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    undo = []
    replaceComplexNumbersFromList(list, "replace -1 with 5+3i", undo)
    assert list == [(5, 3), (2, -3), (4, -5), (5, 3), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]


def testListReal():
    list = [(-1, 0), (2, -3), (4, -5), (-1, 0), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2)]
    assert getListRealNumbersInInterval(list, "list real 0 to 8", len(list)) == [(-1, 0), (-1, 0), (0, 0)]


def testListModulo():
    list = [(-1, 0), (2, -3), (4, -5), (-1, 0), (1, 2), (3, 10), (4, 33), (0, 0), (-7, 1), (3, 2), (3, 4), (6, 8), (4, 3), (8, 6)]
    assert getListModuloNumbers(list, "list modulo > 7") == [(3, 10), (4, 33), (-7, 1), (6, 8), (8, 6)]
    assert getListModuloNumbers(list, "list modulo = 10") == [(6, 8), (8, 6)]
    assert getListModuloNumbers(list, "list modulo > -10") == list


def runTests():
    testExtractComplexNumber()
    testAppendToList()
    testInsertToList()
    testRemoveSingleElement()
    testRemoveMultipleElements()
    testReplace()
    testListReal()
    testListModulo()
    print("All test cases passed!")

runTests()
runCommandBasedApplication()