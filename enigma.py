import string

# Enigma Machine By Caden Siva
# Version 0.1.1
# 2023-03-02


L = string.ascii_uppercase
indexes = [i for i in range(1, 27)]
LETTERS = dict.fromkeys(string.ascii_uppercase, 0)
for l in L:
    LETTERS[l] = ord(l) - 65
class roman:
    # convert a number to roman numerals    
    def toRoman(number):
        if not isinstance(number, type(1)):
            raise TypeError("expected integer, got %s" % type(number))
        if not 0 < number < 4000:
            raise ValueError("Argument must be between 1 and 3999")
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
        result = ""
        for i in range(len(ints)):
            count = int(number / ints[i])
            result += nums[i] * count
            number -= ints[i] * count
        return result

class plugboard:
    foward = {}
    def __init__(self):
        # write an dictionary of the letters of the aplabet as keys and an empty string as values
        self.foward = dict.fromkeys(string.ascii_uppercase, "")

    def connect(self, a, b):
        # connect the letter a to the letter b
        if a == b:
            raise ValueError("Cannot connect a letter to itself")
        if self.foward[a] != "":
            raise ValueError("Cannot connect a letter to two other letters")
        self.foward[a] = b
        self.foward[b] = a

    def showUnusedConnections(self):
        # print out the connections
        for key in self.foward:
            if self.foward[key] == "":
                print(key)
    
    def encode(self, c):
        # return the letter that c is connected to
        if c in self.foward:
            if self.foward[c] != "":
                return self.foward[c]
        return c
        
class configurator:
    RotorConfigs = []
    ReflectorConfigs = []
    roters = []
    reflectors = []
    def __init__(self) -> None:

        self.configureRotors(); self.configureReflectors()

        for i in range(len(self.RotorConfigs)):
            if self.RotorConfigs[i] not in self.roters:
                self.roters.append(roter(self.RotorConfigs[i], i))
        print(len(self.RotorConfigs), " Rotor configurations loaded")

        for config in self.ReflectorConfigs:
            if config not in self.reflectors:
                self.reflectors.append(reflector(config))
        print(len(self.reflectors), " Reflector configurations loaded")

    def getRotor(self, name):
        for rotor in self.roters:
            if rotor.getName() == name:
                return rotor
    def getReflector(self,name):
        if name == "B":
            return self.reflectors[0]
        return self.reflectors[1]

    def configureRotors(self):
        with open("rotorconfig.csv") as file:
            for line in file:
                if line != "":
                    self.RotorConfigs.append(line.strip().split(","))
    def configureReflectors(self):
        try:
            with open('ReflectorModels.csv') as file:
                for line in file:
                    if line != '':
                        line = line.strip().split(',')
                        self.ReflectorConfigs.append(line)
        except:
            with open("/home/siva/code/pyfilesTwo/encyrption/Enigma/ReflectorModels.csv") as file:
                for line in file:
                    if line != '':
                        line = line.strip().split(',')
                        self.ReflectorConfigs.append(line)
            
    def makeRotorAssembly(self, rotorNames) -> list:
        output = []
        names = rotorNames.strip().split(' ')
        for name in names:
            output.append(self.getRotor(name))
        return output

    def printRotorsAndReflectors(self):
        print("Rotors:")
        for rotor in self.roters:
            print(rotor.getName(), end=" ")
        print()
        print("Reflectors:")
        for reflector in self.reflectors:
            print(reflector.getName())
    def reset(self):
        self.RotorConfigs = []
        self.ReflectorConfigs = []
        self.roters = []
        self.reflectors = []

class roter:
    outbound = []
    indexTracker = []
    name = ""
    notch = ''
    def __init__(self, config, name) -> None:
        self.outbound = config
        self.name = roman.toRoman(name+ 1)
        self.indexTracker = [i for i in range(1, 27)]

    def setNotch(self):
        match self.name:
            case "I":
                self.notch = "Q"
            case "II":
                self.notch = "E"
            case "III":
                self.notch = "V"
            case "IV":
                self.notch = "J"
            case "V":
                self.notch = "Z"
            case _:
                self.notch = ("M", 'Z')

    def onNotch(self) -> bool:
        if type(self.notch) == type(tuple):
            return self.outbound[0] in self.notch
        return self.outbound[0] == self.notch
    def getName(self):
        return self.name
    def rotate(self):
        self.outbound = self.outbound[1:] + self.outbound[:1]
        self.indexTracker = self.indexTracker[1:] + self.indexTracker[:1]
    
    def encodefoward(self, c):
        index = LETTERS[c.upper()]
        return self.outbound[index]
    
    def encodebackward(self, c):
        index = self.outbound.index(c.upper())
        return str(chr(index + 65)).upper()

class rotorAssembly:
    rotors = []
    ref = None
    def __init__(self, rotors, ref):
        self.rotors = rotors
        self.ref = ref
    
    def encode(self,c):
        self.rotateAll()
        i = self.passFoward(self.rotors.copy(), c)
        ii = self.ref.encode(i)
        iii = self.passBackward(self.rotors.copy(), ii)
        return iii

    def rotateAll(self):
        if self.rotors[1].onNotch():
            self.rotors[2].rotate()
        if self.rotors[0].onNotch():
            self.rotors[1].rotate()
        self.rotors[0].rotate()

    def passFoward(self,rotors, letter):
        newRotors = rotors.copy()
        if len(newRotors) == 0:
            return letter
        return self.passFoward(newRotors, newRotors.pop(0).encodefoward(letter))
        
    def passBackward(self, rotors, letter):
        newRotors = rotors.copy()
        if len(newRotors) == 0:
            return letter
        return self.passBackward(newRotors, newRotors.pop().encodebackward(letter))

class reflector():
    name = ''
    config = LETTERS.copy()

    def __init__(self, inconfig):
        self.setConfig(inconfig)
        self.name = 'B' if self.config['B'] == 'R' else 'C'

    def setConfig(self, config) -> dict:
        for l in config:
            line = l.split(' ')
            self.config[line[0].upper()] = line[1].upper()
            self.config[line[1].upper()] = line[0].upper()
    def getName(self):
        return self.name

    def encode(self, c):
        if type(self.config[c]) != type(int()):
            return self.config[c.upper()]
        return c.upper()

class housing:
    plugboard = None
    conf = None
    rotors = None
    rotorAssemb = None
    reflector = None

    def __init__(self,conf, rotorNames, reflectorName):
        self.reflector = conf.getReflector(reflectorName)
        self.rotors = conf.makeRotorAssembly(rotorNames)
        self.plugboard = plugboard()
        self.rotorAssemb = rotorAssembly(self.rotors, self.reflector)
    def configurePlugboard(self):
        count = 0
        while count < 10:
            print("enter a connection (A B) or enter ! to quit")
            connection = input("> : ").upper().split(' ')
            if connection[0] == '!':
                break
            self.plugboard.connect(connection[0], connection[1])
            self.plugboard.showUnusedConnections()
            count += 1
    def encodeMSG(self, msg):
        count = 0
        msg = msg.upper().strip().split(' ')
        msg = ''.join(msg)
        output = ""
        for letter in msg:
            output+= self.plugboard.encode(self.rotorAssemb.encode(self.plugboard.encode(letter)))
        
        return output

def human(conf):
    
    conf.printRotorsAndReflectors()
    rot = input("enter a rotor configuration (I II III) (I - IIV): ")

    ref = input('and a reflector (B or C): ')
    enigma = housing(conf,rot.upper(), ref.upper())
    enigma.configurePlugboard()
    msg = input("enter a message to encode/decode: ")
    print(enigma.encodeMSG(msg))

def fileread(conf):
    plugs = []
    index = 0
    with open('config.csv') as file:
        for line in file:
            if line == '':
                raise Exception("cannot have emtpy line in config file")
            match index:
                case 0:
                    rot = line.split(',')
                    newrot = ''
                    for r in rot:
                        newrot += r.strip() + ' '
                    rot = newrot.strip()
                case 1:
                    ref = line.strip()
                case 2:
                    msg = line.strip().upper()
                case _:
                    plugs.append(line.split(','))
            index += 1
    enigma = housing(conf, rot, ref)
    if len(plugs) != 0:
        for plug in plugs:
            enigma.plugboard.connect(plug[0].upper().strip(), plug[1].upper().strip())
    print(enigma.encodeMSG(msg))

def main():
        
        print("-----------------------------------------------------------")
        print(("Welcome\nto\nthe\nEnigma                        by Caden Siva\nMachine\nSimulator").upper())
        print("-----------------------------------------------------------")
        print("Please note that there are a LOT of edge cases that are not\nhandeld grasefully, so please be careful with your input")
        print("If you would like to use a file to configure the machine, please\nuse the file config.csv for consistant results")
        print("-----------------------------------------------------------")
        print("for useage instructions, please see the README.md file")
        print("-----------------------------------------------------------")
        print("===========================================================")
        conf = configurator()
        print("===========================================================")
        user = input("user input, or file read: u/f or ! to exit: ")
        if user == 'u':
            human(conf)
        if user == 'f':
            fileread(conf)
        conf.reset()

if __name__ == "__main__":
    main()
