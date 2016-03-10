#!/usr/bin/env python

import os
import re
import sys
import tkFileDialog
import tkSimpleDialog


def load_file(source, register, stdout):
    filename = tkFileDialog.askopenfilename(
        filetypes=[
            ('All Files', ('.*',)),
            ('Brainf*ck Files', ('.bf',)),
        ],
        initialdir=os.getcwd()
    )

    if not filename:
        return

    source.delete('1.0', 'end')
    with open(filename, 'r') as fin:
        for i, text in enumerate(fin):
            source.insert('end', text.decode('cp932'))  # XXX

    source.focus_set()

    reset(source, register, stdout)


def execute_bf(source, register, stdout, step):
    step_ = int(step.get())
    if step_ is 0:
        step_ = sys.maxint

    source.tag_remove(
        'SELECTED',
        '{}.0+{}c'.format(source.line, source.index),
        '{}.0+{}c'.format(source.line, source.index+1)
    )
    register.tag_remove('SELECTED', '1.0', 'end')

    i = 0
    while source.char and (i < step_):
        if source.char == '+':
            register.array[register.index] += 1
            register.array[register.index] %= 256
        elif source.char == '-':
            register.array[register.index] -= 1
            register.array[register.index] %= 256
        elif source.char == '>':
            register.index += 1
            if not len(register.array) > register.index:
                register.array.append(0)

        elif source.char == '<':
            if register.index:
                register.index -= 1
            else:
                register.array.insert(0, 0)

        elif source.char == '[':
            if register.array[register.index] is 0:
                opened = 1
                while opened:
                    source.index += 1
                    line = '{}.0'.format(source.line)
                    next_ = '{}.0'.format(source.line+1)
                    string = source.get(line, next_)
                    if source.index < len(string):
                        char = string[source.index]
                    else:
                        source.line += 1
                        source.index = 0
                        line = next_
                        next_ = '{}.0'.format(source.line+1)
                        char = source.get(line, next_)[:1]

                    if char == '[':
                        opened += 1
                    elif char == ']':
                        opened -= 1
                    elif char is '':
                        return  # warning

        elif source.char == ']':
            if register.array[register.index] is not 0:
                to_close = 1
                while to_close:
                    source.index -= 1
                    if source.index > -1:
                        line = '{}.0'.format(source.line)
                        next_ = '{}.0'.format(source.line+1)
                        char = source.get(line, next_)[source.index]
                    else:
                        source.line -= 1
                        line = '{}.0'.format(source.line)
                        next_ = '{}.0'.format(source.line+1)
                        string = source.get(line, next_)
                        source.index = len(string) - 1
                        char = string[source.index]

                    if char == '[':
                        to_close -= 1
                    elif char == ']':
                        to_close += 1
                    elif source.line < 1:
                        return  # warning

        elif source.char == ',':
            data = tkSimpleDialog.askstring(
                'Standard Input',
                'input',
            ) + '\\n'
            register.array[register.index] = getchar(data)
        elif source.char == '.':
            stdout.insert(
                'end',
                chr(register.array[register.index])
            )
        else:
            pass

        # rewrite register
        register.delete('1.0', 'end')
        for j in register.array:
            register.insert('end', '[0x{0:0>2X}]'.format(j))

        # search next command
        char = '*'
        while char not in tuple('+-<>[],.') + ('',):
            source.index += 1
            line = '{}.0'.format(source.line)
            next_ = '{}.0'.format(source.line+1)
            string = source.get(line, next_)
            if source.index < len(string):
                char = string[source.index]
            else:
                source.line += 1
                source.index = 0
                line = next_
                next_ = '{}.0'.format(source.line+1)
                string = source.get(line, next_)
                char = string[:1]
        else:
            source.char = char

        i += 1

    source.tag_add(
        'SELECTED',
        '{}.0+{}c'.format(source.line, source.index),
        '{}.0+{}c'.format(source.line, source.index+1)
    )

    register.tag_add(
        'SELECTED',
        '1.0+{}c'.format(register.index*6),
        '1.0+{}c'.format((register.index+1)*6)
    )
    for key, value in source.tagdefs.items():
        source.tag_configure(key, **value)
        register.tag_configure(key, **value)


def reset(source, register, stdout):
    source.line = 0
    source.index = 0
    register.array = [0]
    register.index = 0

    register.delete('1.0', 'end')
    stdout.delete('1.0', 'end')

    register.insert('end', '[0x00]')
    register.tag_add('SELECTED', '1.0+0c', '1.0+6c')
    register.tag_configure('SELECTED', **source.tagdefs['SELECTED'])

    for key in source.tagdefs:
        source.tag_remove(key, '1.0', 'end')

    commands = re.compile(r'[][<>,.+-]')
    comments = re.compile(r'[^][<>,.+-]+')

    ll = 0
    char = {}
    s = '*'
    while s:
        ll += 1
        line = '{}.0'.format(ll)
        next_ = '{}.0'.format(ll+1)
        s = source.get(line, next_)
        if s is '':
            break

        u = comments.search(s)
        while u:
            a, b = u.span()
            source.tag_add(
                'COMMENT',
                line + '+{}c'.format(a),
                line + '+{}c'.format(b)
            )
            u = comments.search(s, b)

        t = commands.search(s)
        if t and char == {}:
            char['index'] = t.start()
            char['line'] = ll

    source.tag_configure('COMMENT', **source.tagdefs['COMMENT'])

    if char == {}:
        return

    source.index = char['index']
    source.line = char['line']
    line = '{}.0'.format(source.line)
    next_ = '{}.0'.format(source.line+1)

    source.char = source.get(line, next_)[source.index]
    source.tag_add(
        'SELECTED',
        '{}.0+{}c'.format(source.line, source.index),
        '{}.0+{}c'.format(source.line, source.index+1)
    )
    source.tag_configure('SELECTED', **source.tagdefs['SELECTED'])

def getchar(string):
    if string[0] == '\\':
        if string[1] in 'abfnrtv':
            return {
                'a': 0x07,
                'b': 0x08,
                't': 0x09,
                'n': 0x0a,
                'v': 0x0b,
                'f': 0x0c,
                'r': 0x0d,
            }[string[1]]
        elif string[1] in 'x':
            num = '0' + re.search(r'^[0-9A-Fa-f]{,2}', string[2:]).group()
            return int(num, 16)
        elif string[1] in '01234567':
            num = re.search(r'^[0-7]{1,3}', string[1:]).group()
            return int(num, 8)
        elif string[1] in ('"', "'", '\\'):
            return ord(string[1])
        else:  # Ignore \u...., \U........, and \N{...}
            return 0x5c
    else:
        return ord(string.encode('utf-8')[0])  # XXX
