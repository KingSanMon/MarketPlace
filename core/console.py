class Consoles:

    def log(self, text, type = 2):
        if type == 0:
            print("\033[31m {}" .format(text))
        if type == 1:
            print("\033[33m {}" .format(text))
        if type == 2:
            print("\033[32m {}" .format(text))

console = Consoles()