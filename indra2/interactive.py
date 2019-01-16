"""
interactive.py:
Setup an interesting interactive env in which to play
and try out new features.
"""

from tests.test_entity import *
from tests.test_composite import *
from itime import *

newton = create_newton()
leibniz = create_leibniz()
hardy = create_hardy()
ramanujan = create_ramanujan()
littlewood = create_littlewood()
ramsey = create_ramsey()
calc = create_calcguys()
camb = create_cambguys()
maths = create_mathguys()
gauss = Entity("Gauss")
euler = Entity("Euler")
germans = Composite("Germans",
                    members={gauss.name: gauss,
                             euler.name: euler})
maths += germans
math_hist = Time("History", members={maths.name: maths})
