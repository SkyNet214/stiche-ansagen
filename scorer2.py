input("[START]")
import time, sys, os, platform, pickle

testvar = "lie"
c, r = 1, 0
doSave = False
filename: str
calcbool = False

def clear():
    OS = platform.system()
    if OS == 'Windows':
        cc = 'cls'
    elif OS == 'Linux':
        cc = 'clear'
    else:
        cc = ''
    os.system(cc)

def binInput(msg):
    try:
        a = str(input(msg))
        if a == 'y':
            return True
        if a == 'n':
            return False
        else: raise Exception
    except:
        input("[ERROR] Answer must be 'y' or 'n'")
        return binInput(msg)

def intInput(message):
    try:
      num = int(input(message))
      return num
    except Exception as e:
      print("[ERROR] Please type in an integer.")      
      return intInput(message)

def strInput(message):
	try:
		string = str(input(message))
		return string
	except:
		input("[ERROR] Please type in a string")
		return strInput(message)

class Player:

    players = []

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.stiche_a = 0
        self.stiche_m = 0

    def addP(self, points):
        self.points += points

    def setP(self, points):
        self.points = points

    @classmethod
    def arrangePlayersList(cls):
        clear()
        order = []
        for player in cls.players:
            pos = intInput(player.name + " position > ")
            if pos < 1 or pos > len(cls.players) or pos-1 in order:
                input("[ERROR] Position isn't available; Starting again")
                order = []
                return cls.arrangePlayersList()
            order.append(pos-1)
            print(order)
        cls.players = [cls.players[i] for i in order]
        clear()

def createPlayerObjects():
    clear()
    n = intInput("Number of players > ")
    if n < 1:
        input("[ERROR] Number of players must be bigger than 0")
        return createPlayerObjects()
    clear()
    for i in range(0, n):
        name = strInput("Name of player " + str(i+1) + " > ")
        Player.players.append(Player(name))

def intro():
    clear()
    intro = "This is a scorer for the card game 'Stiche ansagen' by Niklas Rheinlaender.\nPlease note, that this scorer is only made for 2-6 players.\nLet's begin! :)\n"

    for char in intro: # typing effect
        time.sleep(0.05)
        sys.stdout.write(char)
        sys.stdout.flush()
    time.sleep(2)
    clear()


def playerInput():
    print(f"\n########## Runde {c}/{r} ##########\n")
    for p in Player.players:
        p.stiche_a = intInput("Stiche announced by " + p.name + " > ")
    input("[ENTER]")
    clear()
    for p in Player.players:
        p.stiche_m = intInput("Stiche made by " + p.name + " > ")
    input("[ENTER]")
    pattern = [i for i in range(1, len(Player.players))]
    pattern.append(0)
    Player.players = [Player.players[i] for i in pattern]
    clear()

def calc():
    global calcbool
    if not calcbool:
        for p in Player.players:
            if p.stiche_a == p.stiche_m:
                p.addP((p.stiche_m + 10))
            else:
                p.addP(p.stiche_m)
        calcbool = True



def printScore():
    clear()
    score = [p for p in Player.players]
    score.sort(key=lambda x: x.points, reverse = True)
    print("\n########## SCORE (Round {}/{}) ##########\n".format(c,r))
    for s in score:
        print(s.name,f"({s.stiche_m}/{s.stiche_a})", ": ", s.points, end="\n")
    input("\n#########################################\n")
    clear()

def terminate():
    print("trying to quit")
    exit()

def displayHelp():
    msg =   """
    next    go to next round
    chOrd   change order of players
    setP    set points of a player
    setS1   set 'angesagte Stiche'
    setS2   set 'gemachte Stiche'
    score   show the score
    setR    set number of rounds
    setC    set current round
    exit    exit the game
    help    show this information\n"""
    print(msg)

def setR():
    global r
    r = intInput("Number of rounds > ")

def setC():
    global c
    c = intInput("Current round > ")

def load(filename):
    global c, r
    with open(filename, 'rb') as f:
        Player.players, r, c = pickle.load(f)
        f.close()

def save():
    global filename
    if doSave:
        with open(filename, 'wb') as f:
            pickle.dump([Player.players, r, c], f, protocol=2)

def loadStat():
    a = binInput("Do you want to load a savefile? [y/n] ")
    if a:
        filename = strInput("Filename > ")
        try:
        	load(filename)
        except:
            print("[ERROR] couldn't load file")
            return loadStat()
    return a

def saveStat():
    global doSave, filename
    a = binInput("Do you want to save the game every round? [y/n] ")
    if a:
        filename = strInput("Savefile name > ")
        try:
            save()
            doSave = True
        except:
            print("[ERROR] couldn't find or create savefile")
            return saveStat()
    else: doSave = False

def initiateGame():
    global r
    clear()
    intro()
    if not loadStat():
        r = intInput("Number of rounds > ")
        createPlayerObjects()
    saveStat()
    clear()

def CLI():
    global c, r
    while True:
        dic = {
        "chOrd"     : Player.arrangePlayersList,
        "setP"      : None, #setPoints,
        "setS1"     : None,
        "setS2"     : None,
        "score"     : printScore,
        "help"      : displayHelp,
        "setR"      : setR,
        "setC"      : setC,
        "calc"      : calc
        }
    
        cmd = strInput(f"({c}/{r})~$ ")
    
        if cmd == "exit":
            sys.exit()
        elif cmd == "next":
            clear()
            return
    
        try:
            dic[cmd]()
        except:
            print("[ERROR] unknown input")
            return CLI()

def loop():
    global c, r, calcbool
    while c <= r:
        calcbool = False
        clear()
        playerInput()
        CLI()
        c+=1
        save()

def main():
    try:
        initiateGame()
        CLI()
        loop()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()