"""
user.py
Manages the user for the Indra system.
"""

# import logging
# we are going to do some shenanigans so we can use clint if present
#  and work around if not
MENU = "menu"
PROMPT = "prompt"
ERROR = "error"
INFO = "info"
text_colors = None
clint_present = True
try:
    from clint.textui import colored, puts, indent
    text_colors = {MENU: colored.blue,
                   PROMPT: colored.magenta,
                   ERROR: colored.red,
                   INFO: colored.black}
except ImportError:
    clint_present = False
    text_colors = {MENU: None,
                   PROMPT: None,
                   ERROR: None,
                   INFO: None}

import indra.entity as ent
import indra.prop_args as pa

# user types
TERMINAL = pa.TERMINAL
IPYTHON = pa.IPYTHON
IPYTHON_NB = pa.IPYTHON_NB
WEB = pa.WEB

run_output = ""

def ask(msg, default=None, limits=None):
    answer = None
    rng_msg = ""
    if limits is not None:
        (low, high) = limits
        rng_msg = " [" + str(low) + "-" + str(high) + "]"
    if default is not None:
        msg += " (" + str(default) + ")"
    msg += rng_msg + " "
    if clint_present:
        puts(text_colors[PROMPT](msg), newline=False)
    else:           
        print(msg, end='')
    
    return input()


def tell(msg, type=INFO, indnt=0, utype=TERMINAL, text_output=None):
    if utype == WEB:
        return text_output + msg + "\n"
    else:
        if indnt <= 0:
            if clint_present:
                puts(text_colors[type](msg))
            else:
                print(msg)
        else:
            if clint_present:
                with indent(indnt):
                    puts(text_colors[type](msg))
            else:
                for i in range(0, indnt):
                    msg = '  ' + msg
                print(msg)

class User(ent.Entity):
    """
    We will represent the user to the system as another entity.
    """
    def __init__(self, nm, utype=TERMINAL):
        super().__init__(nm)
        self.utype = utype
        self.text_output = ''

    def tell(self, msg, type=INFO, indnt=0):
        """
        Screen the details of output from models.
        """
        if msg and self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]:
            return tell(msg, type=type, indnt=indnt, utype=self.utype)
        elif msg and self.utype == WEB:
            self.text_output = tell(msg, type=type, indnt=indnt, 
                                    utype=self.utype, 
                                    text_output=self.text_output)
            return self.text_output

    def ask_for_ltr(self, msg):
        """
        Screen the details of input from models.
        """
        choice = self.ask(msg)
        return choice.strip()

    def ask(self, msg):
        """
        Screen the details of input from models.
        """
        assert self.utype in [TERMINAL, IPYTHON, IPYTHON_NB, WEB]
        if(self.utype in [TERMINAL, IPYTHON, IPYTHON_NB, WEB]):
            return ask(msg)
