NUMOFCHARS = 6

def unique_str(str):
    for w in str:
        if str.count(w) != 1:
            return False
    return True

newf=open("sixwords.txt", "w+")
with open('words.txt', 'r') as f:
    fl = f.readlines()
    for x in fl:
        temp = x[:-1] # remove new line character from the end
        temp = temp.upper()
        if len(temp) == NUMOFCHARS and temp.isalpha() == True:
            if unique_str(temp) == True:
                newf.write(temp + "\n")