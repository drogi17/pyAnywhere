class Colors:
    def __init__(self, color=None):
        if not color:
            print(color)
        else:
            self.text       = str('\033[%sm' % (int(color) + 30))
            self.background = str('\033[%sm' % (int(color) + 40))

def ok_text(string):
    green = Colors(2)
    white = Colors(7)
    return green.text + string + white.text

def error_text(string):
    red   = Colors(1)
    white = Colors(7)
    return red.text + string + white.text

# black       = Colors(0)
red         = Colors(1)
green       = Colors(2)
yellow      = Colors(3)
blue        = Colors(4)
purple      = Colors(5)
turquoise   = Colors(6)
white       = Colors(7)
