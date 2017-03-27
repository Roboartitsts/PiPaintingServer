class ColorRGB:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.cyan = 0
        self.magenta = 0
        self.yellow = 0
        self.black = 0
        self.white = 0

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
