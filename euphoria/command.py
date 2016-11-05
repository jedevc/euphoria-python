
import re as _re

class Token(str):
    """
    A Token is a string with an offset into its source attached.
    """

    def __new__(cls, data, offset):
        ret = super().__new__(cls, data)
        ret.offset = offset
        return ret

    @classmethod
    def split(cls, string):
        """
        split(string) -> list

        Split the given string into Tokens, similarly to str.split().
        """

        parts = _re.split('(\s+)', string)
        offset = 0
        ret = []

        for n, p in enumerate(parts):
            if not n % 2:
                ret.append(Token(p, offset))
            offset += len(p)

        # Leading and trailing empty tokens are removed.
        if not ret[0]: del ret[0]
        if ret and not ret[-1]: del ret[-1]

        return ret

class Command:
    """
    The Command class allows you to parse and read bot commands. This includes
    the main command, the arguments and the flags.
    """

    def __init__(self, text):
        self.text = text

        self.command = ""
        self.flags = {}
        self.args = []

    def parse(self):
        """
        parse() -> None

        Perform the parsing.
        """

        parts = Token.split(self.text)

        if len(parts) == 0:
            return

        if parts[0][0] == '!':
            self.command = parts[0][1:]

        split = 1
        for p in range(1, len(parts)):
            if parts[p][0] == '-':
                if '=' in parts[p]:
                    flag = parts[p][1:].split('=')
                    self.flags[flag[0]] = flag[1]
                else:
                    self.flags[parts[p][1:]] = None
                split = p + 1
            else:
                break

        self.args = parts[split:]
