"""
This is the test suite for composite.py.
"""

from collections import OrderedDict

from unittest import TestCase, main

from indra2.composite import Composite
from indra2.tests.test_agent import create_hardy, create_newton
from indra2.tests.test_agent import create_ramanujan, create_littlewood
from indra2.tests.test_agent import create_ramsey, create_leibniz

N = "Newton"
R = "Ramanujan"
L = "Leibniz"
H = "Hardy"
NL = N + L
LN = L + N
HR = H + R
LR = "LittlewoodRamsey"


def match_name(agent, name):
    return agent.name == name


def max_duration(agent, duration):
    return agent.duration <= duration


def create_calcguys():
    n = create_newton()
    l = create_leibniz()
    return Composite("Calculus guys",
                     members=OrderedDict([(n.name, n), (l.name, l)]))


def create_cambguys():
    h = create_hardy()
    r = create_ramanujan()
    return Composite("Cambridge guys",
                     members=OrderedDict([(h.name, h), (r.name, r)]))


def create_cambguys2():
    l = create_littlewood()
    r = create_ramsey()
    return Composite("Other Cambridge guys",
                     members=OrderedDict([(l.name, l), (r.name, r)]))


def create_mathguys():
    calc = create_calcguys()
    camb = create_cambguys()
    return Composite("Math guys",
                     members=OrderedDict([(calc.name, calc),
                                          (camb.name, camb)]))

def create_mem_str(comp):
    s = ""
    for agent in comp:
        s += agent  # this will collect the names of the members
    return s


class CompositeTestCase(TestCase):
    def test_eq(self):
        calc1 = create_calcguys()
        camb = create_cambguys()
        self.assertEqual(calc1, calc1)
        self.assertNotEqual(camb, calc1)

    def test_str(self):
        name = "Ramanujan"
        c = Composite(name)
        self.assertEqual(name, str(c))

    def test_repr(self):
        # this test has to be written!
        # self.assertEqual(rep, repr(agent))
        pass

    def test_len(self):
        camb = create_cambguys()
        self.assertEqual(len(camb), 2)

    def test_get(self):
        camb = create_cambguys()
        self.assertEqual(camb["Hardy"], create_hardy())

    def test_set(self):
        camb = create_cambguys()
        camb["jel"] = create_littlewood()
        self.assertEqual(camb["jel"], create_littlewood())

    def test_contains(self):
        camb = create_cambguys()
        self.assertTrue("Hardy" in camb)

    def test_iter(self):
        self.assertEqual(create_mem_str(create_calcguys()), NL)

    def test_reversed(self):
        calc = create_calcguys()
        s = ""
        for guy in reversed(calc):
            s += guy
        self.assertEqual(s, LN)

    def test_mul(self):
        camb = create_cambguys()
        newt = create_newton()
        camb[newt.name] = newt
        calc = create_calcguys()
        mathguys = calc * camb
        self.assertEqual(create_mem_str(mathguys), N)

    def test_imul(self):
        camb = create_cambguys()
        mathguys = create_calcguys() + camb
        self.assertEqual(create_mem_str(mathguys), NL + HR)
        mathguys *= camb  # should drop out calc!
        self.assertEqual(create_mem_str(mathguys), HR)

    def test_add(self):
        calc = create_calcguys()
        camb = create_cambguys()
        mathguys = calc + camb
        self.assertEqual(create_mem_str(mathguys), NL + HR)
        mathguys = calc + camb + create_cambguys2()
        self.assertEqual(create_mem_str(mathguys), NL + HR + LR)
        # ensure we did not change original group:
        self.assertEqual(create_mem_str(calc), NL)
        # let's make sure set union does not dupe members:
        camb_self_union = camb + camb
        self.assertEqual(create_mem_str(camb_self_union), HR)
        # now let's add an atom rather than a composite:
        calch = calc + create_hardy()
        self.assertEqual(create_mem_str(calch), NL + H)

    def test_iadd(self):
        camb = create_cambguys()
        # let's make sure set union does not dupe members:
        camb += camb
        self.assertEqual(create_mem_str(camb), HR)
        # now test adding new members:
        camb += create_cambguys2()
        self.assertEqual(create_mem_str(camb), HR + LR)
        # now test adding an atomic entity:
        camb += create_newton()
        self.assertEqual(create_mem_str(camb), HR + LR + N)

    def test_sub(self):
        calc = create_calcguys()
        mathguys = calc + create_cambguys() + create_cambguys2()
        cambguys = mathguys - calc
        self.assertEqual(create_mem_str(cambguys), HR + LR)
        # now test deleting an atom:
        hardygone = cambguys - create_hardy()
        self.assertEqual(create_mem_str(hardygone), R + LR)
        # make sure we didn't change original group:
        self.assertEqual(create_mem_str(cambguys), HR + LR)
        # delete something that ain't there:
        cambguys = cambguys - calc
        self.assertEqual(create_mem_str(cambguys), HR + LR)

    def test_isub(self):
        calc = create_calcguys()
        mathguys = calc + create_cambguys() + create_cambguys2()
        mathguys -= calc
        self.assertEqual(create_mem_str(mathguys), HR + LR)
        # now test deleting an atom:
        mathguys -= create_hardy()
        self.assertEqual(create_mem_str(mathguys), R + LR)

    def test_call(self):
        mathguys = create_cambguys() + create_calcguys()
        acts = mathguys()
        self.assertEqual(acts, 3)  # hardy is passive!

    def test_subset(self):
        calc = create_calcguys()
        just_n = calc.subset(match_name, "Newton", name="Just Newton!")
        self.assertEqual(create_mem_str(just_n), N)
        just_l = calc.subset(max_duration, 25, name="Just Leibniz!")
        self.assertEqual(create_mem_str(just_n), N)

    def test_magnitude(self):
        pass


if __name__ == '__main__':
    main()
