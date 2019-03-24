import sys
import re

def choiceTypeCheck(choiceType):
    """checking key-in character
    """
    return choiceType != "i" and \
            choiceType != "e" and \
            choiceType != "all" and \
            choiceType != "quit"

def choiceNextCheck(choiceNext):
    """checking key-in character
    """
    return choiceNext != "d" and \
        choiceNext != "q"

def interactive_input_interface(wnidMapWords, inputString):
    """interactive CLI interface
    """
    keywords = [i.strip() for i in inputString.split('+')]

    choiceLines = []
    idx = 0
    for val in wnidMapWords:
        for keyword in keywords:
            if re.match('(?:(?:.*?([^ ,]+ ' + keyword + '$))|' +   # adj keyword
                           '(?:.*?([^ ,]+ ' + keyword + '),)|' +   # adj keyword,
                           '(^' + keyword + '$)|' +                # keyword
                           '(^' + keyword + ',)|' +                # keyword,
                           '(?:.*? (' + keyword + '$))|' +         # , keyword
                           '(?:.*? (' + keyword + '),))', val[1]): # , keyword,
                choiceLines.append(val)
                break

    if not choiceLines:
        sys.exit(0)

    for idx, choiceLine in enumerate(choiceLines):
        print(f"{idx:5} : {choiceLine[1]}")

    while choiceTypeCheck(inputString):
        inputString = input("How to choose lines?[(i)nclude/(e)xclude/all/quit]: ")
    choiceType = inputString

    choiceIndexes = []
    if choiceType == "i":
        print("You use including choice.")
    elif choiceType == "e":
        print("You use excluding choice.")
    elif choiceType == "all":
        inputString = "ok"
        choiceIndexes = [i for i in range(len(choiceLines))]
        print("You choose all.")
    else:
        print("You choose to leave.")
        sys.exit(0)

    while inputString != "ok":
        inputString = input("Please key in the index(es) of the list[ok/check]: ")
        # valid characters
        if inputString.isnumeric():
            intInputString = int(inputString)
            # valid index range
            if intInputString >= 0 and intInputString < len(choiceLines):
                # exclude the same input
                if intInputString not in choiceIndexes:
                    choiceIndexes.append(intInputString)
        elif inputString == "check":
            for val in choiceIndexes:
                print(f"{val:5} : {choiceLines[val][1]}")
        elif inputString == "ok":
            pass
        else:
            print("Please enter the index(numeric) of the list.")

    # reverse the choice index(es)
    if choiceType == "e":
        tmp = choiceIndexes.copy()
        choiceIndexes = [i for i in range(len(choiceLines)) if i not in tmp]

    print("You choiced: ")
    for val in choiceIndexes:
        print(f"{val:5} : {choiceLines[val][1]}")

    while choiceNextCheck(inputString):
        inputString = input("Please key in (d)ownload to starting download or (q)uit to leave[d/q]: ")

    if inputString == "d":
        print("Download starting")
        return [choiceLines[val][0] for val in choiceIndexes]
    else:
        print("You choose to leave.")
        return None
