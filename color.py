class Color:
    def __init__(self):
        self.red = None
        self.green = None
        self.blue = None
        self.cyan = None
        self.magenta = None
        self.yellow = None
        self.black = None
        self.white = None

    def setRGB(self, rgb):
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]

    def setCMYK(self, cmyk):
        self.cyan = cmyk[0]
        self.magenta = cmyk[1]
        self.yellow = cmyk[2]
        self.black = cmyk[3]
        self.white = cmyk[4]

    def rgb2cmyk(self):
        rp = self.red/255.0
        gp = self.green/255.0
        bp = self.blue/255.0
        self.black = 1.0 - max([rp, gp, bp])
        self.white = 1.0 - self.black
        if self.black != 1.0:
            self.cyan = (1.0 - rp - self.black) / (1.0 - self.black)
            self.magenta = (1.0 - gp - self.black) / (1.0 - self.black)
            self.yellow = (1.0 - bp - self.black) / (1.0 - self.black)

    def cmyk2rgb(self):
        self.red = 255.0 * (1 - self.cyan) * (1 - self.black)
        self.green = 255.0 * (1 - self.magenta) * (1 - self.black)
        self.blue = 255.0 * (1 - self.yellow) * (1 - self.black)

    def getRGB(self):
        return [self.red, self.green, self.blue]

    def getCMYK(self):
        return [self.cyan, self.magenta, self.yellow, self.black, self.white]

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.getRGB() == other.getRGB() or self.getCMYK() == other.getCMYK()

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(tuple([self.red, self.green, self.blue]))

