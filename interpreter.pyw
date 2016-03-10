#!/usr/bin/env python

import os
import sys
import ScrolledText
import Tkinter

from commands import *



class SourceCode(ScrolledText.ScrolledText):
    def __init__(self, master=None, **kwargs):
        ScrolledText.ScrolledText.__init__(self, master, **kwargs)
        self.line = 1
        self.index = 0
        self.char = '*'

        self.tagdefs = {
            'SELECTED': {
                'foreground': '#ff0b3a', 'background': '#ffffff',
                'font': ('Consolas', 10, 'bold underline'),
            },
            'COMMENT': {
                'foreground': '#969896', 'background': '#ffffff',
                'font': ('Consolas', 10),
            },
        }

class Register(ScrolledText.ScrolledText):
    def __init__(self, master=None, **kwargs):
        ScrolledText.ScrolledText.__init__(self, master, **kwargs)
        self.array = [0]
        self.index = 0


root = Tkinter.Tk()
root.option_add('*font', ('Consolas', 10))
root.title('Brainf*ck interpreter')

frame_stdout = Tkinter.LabelFrame(
    root,
    text='Standart output',
    width=64,
    height=12,
)

stdout = ScrolledText.ScrolledText(
    frame_stdout,
    width=64,
    height=12,
)

frame1 = Tkinter.Frame(root)

frame_source = Tkinter.LabelFrame(
    frame1,
    text='Source code',
    width=32,
    height=16,
)

source = SourceCode(
    frame_source,
    width=32,
    height=16,
)

frame2 = Tkinter.Frame(frame1)

frame_register = Tkinter.LabelFrame(
    frame2,
    text='Register',
    width=32,
    height=16,
)

register = Register(
    frame_register,
    width=32,
    height=16,
)

frame3 = Tkinter.Frame(frame2)

frame_step = Tkinter.LabelFrame(
    frame3,
    text='# of steps',
    width=8,
    height=1,
)

step = Tkinter.Spinbox(
    frame_step,
    from_=0,
    to=sys.maxint,
    increment=1,
    width=8,
)

execute = Tkinter.Button(
    frame3,
    text='Execute',
    width=24,
    height=2,
    command=lambda: execute_bf(source, register, stdout, step),
)

menu0 = Tkinter.Menu(root)
root.configure(menu=menu0)

menu1 = Tkinter.Menu(menu0, tearoff=False)
menu1.add_command(
    label='Open', under=0,
    command=lambda: load_file(source, register, stdout),
)
menu1.add_command(
    label='Reset', under=0,
    command=lambda: reset(source, register, stdout),
)
menu1.add_separator()
menu1.add_command(label='Exit', under=0, command=sys.exit)
menu0.add_cascade(label='File', under=0, menu=menu1)


execute.pack(
    side='left',
    fill='both',
    expand=True,
)
step.pack(
    fill='both',
    expand=True,
)
frame_step.pack(
    side='right',
    fill='x',
    expand=True,
)
frame3.pack(
    side='bottom',
    fill='x',
)
register.pack(
    fill='both',
    expand=True,
)
frame_register.pack(
    side='top',
    fill='both',
    expand=True,
)
frame2.pack(
    side='right',
    fill='both',
    expand=True,
)
source.pack(
    fill='both',
    expand=True,
)
frame_source.pack(
    side='left',
    fill='both',
    expand=True,
)
frame1.pack(
    side='top',
    fill='both',
    expand=True,
)
stdout.pack(
    fill='both',
    expand=True,
)
frame_stdout.pack(
    side='bottom',
    fill='both',
    expand=True,
)

iconfile = os.path.join(
    os.path.dirname(__file__),
    'idle_16.ico'
)
root.wm_iconbitmap(default=iconfile)


if __name__ == '__main__':
    root.mainloop()
