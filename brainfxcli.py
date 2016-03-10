#!/usr/bin/env python

import re
import sys
from StringIO import StringIO


class BrainFxck(object):
    def __init__(self, fin):
        self.fin = fin
        self.register = [0]
        self.index = 0

    def parse(self):
        char = self.fin.read(1)
        while char:
            if char not in '+-<>[],.':
                pass
            elif char == '+':
                self.register[self.index] += 1
                self.register[self.index] %= 256
            elif char == '-':
                self.register[self.index] -= 1
                self.register[self.index] %= 256
            elif char == '>':
                self.index += 1
                if not len(self.register) > self.index:
                    self.register.append(0)
            elif char == '<':
                if self.index:
                    self.index -= 1
                else:
                    self.register.insert(0, 0)
            elif char == '[':
                if self.register[self.index] == 0:
                    opened = 1
                    while char and opened:
                        if opened:
                            char = self.fin.read(1)

                        if char == '[':
                            opened += 1
                        elif char == ']':
                            opened -= 1
                    else:
                        if not char:
                            raise SyntaxWarning  # TODO

                    continue
            elif char == ']':
                if not self.register[self.index] == 0:
                    to_close = 1
                    while char and to_close:
                        if to_close:
                            self.fin.seek(-2, 1)
                            char = self.fin.read(1)

                        if self.fin.tell() == 1:
                            if to_close:
                                raise SyntaxError  # TODO

                        if char == '[':
                            to_close -= 1
                        elif char == ']':
                            to_close += 1

        
                    continue
            elif char == ',':
                data = raw_input('\nInput: ') + '\n'  # TODO
                self.register[self.index] = ord(data[0])
            elif char == '.':
                sys.stdout.write(chr(self.register[self.index]))

            char = self.fin.read(1)


def main():
    usage = 'Usage: brainfxcli.py { brainfxck-code | -i <brainfxck-file> }'
    if not sys.argv[1:]:
        print usage
        return 1

    if sys.argv[1] == '-i':
        if not sys.argv[2:]:
            print usage
            return 1
        try:
            fin = open(sys.argv[2], 'r')
        except IOError as e:
            print e
            return 2
    else:
        code = sys.argv[1]
        fin = StringIO(code)

    BrainFxck(fin).parse()


if __name__ == '__main__':
    main()
