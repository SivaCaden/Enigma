import string



class roman:
    # convert a number to roman numerals    

    def toRoman(number):
        # convert a number to roman numerals
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

    def showConnections(self):
        # print out the connections
        for key in self.foward:
            if self.foward[key] != "":
                print(key, "is connected to", self.foward[key])
    
    def encode(self, c):
        # return the letter that c is connected to
        if c in self.foward:
            if self.foward[c] != "":
                return self.foward[c]
        return c
        
class roters:
    LETTERS = string.ascii_uppercase
    configs = None
    roters = []
    def __init__(self) -> None:
        self.configs = []
        with open("rotorconfig.csv") as file:
            for line in file:
                if line != "":
                    self.configs.append(line.strip().split(","))
            print(len(self.configs), " configurations loaded")
        for i in range(len(self.configs)):
            self.roters.append(roter(self.configs[i], i))

class roter:
    inbound = roters.LETTERS
    outbound = []
    name = ""
    notch = ''
    def __init__(self, config, name) -> None:
        self.outbound = config
        self.name = roman.toRoman(name+ 1)
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

    def getName(self):
        return self.name
    def rotate(self):
        raise NotImplementedError



class testing:
    def letters(self):
        print(string.ascii_uppercase)
    def settingRoaters(self):
        roters()

class running():
    def run(self):
        userinput = input("Enter a message: ").upper()
        plugboard1 = plugboard()
        plugboard1.connect("A", "B")
        plugboard1.connect("C", "D")
        for letter in userinput:
            print(plugboard1.encode(letter), end="")


def main():
    testing().settingRoaters()

    
    

main()
