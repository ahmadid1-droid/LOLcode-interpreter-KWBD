# CMSC 124 milestone 1

KEYWORDS = [
    "HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR",
    "I HAS A", "ITZ", "R", "AN", "SUM OF", "DIFF OF", "PRODUKT OF",
    "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF",
    "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM",
    "DIFFRINT", "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH",
    "O RLY?", "YA RLY", "MEBBE", "NO WAI", "OIC", "WTF?", "OMG",
    "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE",
    "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR",
    "I IZ", "MKAY"
]
# check longer keywords first
KEYWORDS = sorted(KEYWORDS, key=len, reverse=True)
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

def isDigits(text):
    if text == "":
        return False
    for char in text:
        if char not in DIGITS:
            return False
    return True


def classify(word):
    if word in ["WIN", "FAIL"]:
        return "TROOF Literal"
    if word in ["NOOB", "NUMBR", "NUMBAR", "YARN", "TROOF"]:
        return "TYPE Literal"

    # check number, removing the negative sign first
    number=word
    if number.startswith("-"):
        number = number[1:]
    if isDigits(number):
        return "NUMBR Literal"
    parts =number.split(".")
    if len(parts)==2:
        if (parts[0] == "" or isDigits(parts[0])) and isDigits(parts[1]):
            return "NUMBAR Literal"

    # identifier starts with a letter
    if word != "" and word[0] in LETTERS:
        for char in word:
            if char not in LETTERS + DIGITS + "_":
                return "Invalid"
        return "Identifier"
    return "Invalid"


def scan(source):
    tokens=[]
    errors = []
    commentLine= 0
    lineNum = 0

    for line in source.splitlines():
        lineNum+=1
        i=0
        while i < len(line):
            if line[i].isspace():
                i += 1
                continue

            # skip comment body until TLDR
            if commentLine != 0:
                if line[i:].split()[0] == "TLDR":
                    tokens.append(("TLDR", "Keyword", lineNum))
                    commentLine = 0
                break

            start= i

            # read string, keeping the spaces inside
            if line[i] == '"':
                i += 1
                while i < len(line) and line[i] != '"':
                    i += 1
                if i == len(line):
                    errors.append((lineNum, "Missing closing quote."))
                    break
                i += 1
                tokens.append((line[start:i], "YARN Literal", lineNum))
                continue

            # check keywords
            keyword = ""
            for candidate in KEYWORDS:
                end = i+len(candidate)
                if line[i:end] == candidate:
                    if end == len(line) or line[end].isspace() or line[end] in '\"+':
                        keyword = candidate
                        break

            if keyword != "":
                tokens.append((keyword, "Keyword", lineNum))
                i+= len(keyword)
                if keyword == "BTW":
                    break
                if keyword == "OBTW":
                    if line[:start].strip() != "":
                        errors.append((lineNum, "OBTW must start on its own line."))
                    commentLine = lineNum
                    break
                if keyword == "TLDR":
                    errors.append((lineNum, "TLDR without OBTW."))
                continue

            if line[i] == "+":
                tokens.append(("+", "Output separator", lineNum))
                i += 1
                continue

            # read word and check its type
            while i < len(line):
                if line[i].isspace() or line[i] in '\"+':
                    break
                i += 1
            word=line[start:i]
            tokenType= classify(word)
            if tokenType == "Invalid":
                errors.append((lineNum, "Invalid lexeme: " + word))
            else:
                tokens.append((word, tokenType, lineNum))

    if commentLine != 0:
        errors.append((commentLine, "Missing TLDR for block comment."))
    return tokens, errors


def main():
    # open file
    fileName = input("Enter the .lol file path: ").strip()
    try:
        with open(fileName, "r", encoding="utf-8-sig") as fp:
            source = fp.read()
    except (OSError, UnicodeError) as error:
        print("Cannot read file:", error)
        return

    # get tokens
    tokens,errors = scan(source)


    # print results
    print("\nLine  Classification        Lexeme")
    print("-" * 65)
    for word, tokenType, line in tokens:
        print(f"{line}{tokenType}{word}")
    for line, message in errors:
        print("Error on line", str(line) + ":", message)
    print("\nTokens:", len(tokens), "| Lexical errors:", len(errors))


if __name__ == "__main__":
    main()
