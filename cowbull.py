import random
WORDLENGTH = 6
WORDFILE = "sixwords.txt"
FILELENGTH = 17443


def findcowsandbulls(inputword, guessword):
    word = inputword.upper()
    bull, cow = 0, 0
    for w in word:  # type: object
        if guessword.find(w) == -1:
            continue
        if word.find(w) == guessword.find(w):
            bull = bull + 1
        else:
            cow = cow + 1
    return cow, bull


def validateword(inputword):
    if len(inputword) != WORDLENGTH:
        print("Error - enter a word with exactly six characters")
        return False
    if inputword.isalpha() == False:
        print ("Error - enter only alphabetic characters")
        return False
    for w in inputword:
        if inputword.count(w) > 1:
            print("Error - enter a six letter word with unique letters")
            return False
    return True


def randomword():
    i = random.randint(1,FILELENGTH)
    with open (WORDFILE, "r") as f:
        line = f.readlines()[i]
        temp = line[:-1]
        return temp


def readinputword():
    inputword = raw_input("Enter a six letter word  ")
    while (validateword(inputword) != True):
        inputword = raw_input("Enter a six letter word  ")
    return inputword

def main():
    guessword = randomword()
    cow, bull, attempts = 0,0,0
    while bull != WORDLENGTH:
        inputword = readinputword()
        attempts = attempts + 1
        cow, bull = findcowsandbulls(inputword, guessword)
        print "cow = ", cow , "bull = ", bull
    print ("You cracked the word in ", +attempts, "chances!")

main()
