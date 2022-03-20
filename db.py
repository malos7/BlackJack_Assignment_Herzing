# Jordan McClure "Blackjack Final"

MONEYFILE = "money.txt"

def readMoney():
    userMoney = 100.00
    try:
        with open(MONEYFILE) as file:
            for line in file:
                userMoney = line
            return userMoney
    except FileNotFoundError:
        print("File not found. Setting user money to 100.00")
        return userMoney

def writeMoney(userMoney):
    with open(MONEYFILE, "w") as file:
        userMoney = str(userMoney)
        file.write(userMoney)
