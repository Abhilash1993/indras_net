"""
prehension.py
The way agents interact is through prehensions.
entity.py currently has another notion of prehension: that one
and this one must be combined in the future.
The base implementation of a prehension is as a vector.
As of the moment, this is essentially a wrapper around numpy's vector
functions. But the reason to do it that way is because other models might
want a prehension that is NOT a vector.
Sub-class this to instantiate another implementation.
"""

import math
import numpy as np
# import logging

# x and y indices
X = 0
Y = 1

# Set up constants for some common vectors: this will save time and memory.
X_VEC = np.array([1, 0])
Y_VEC = np.array([0, 1])
NULL_VEC = np.array([0, 0])
NEUT_VEC = np.array([.7071068, .7071068])


class Prehension:
    """
    All prehensions must have the following properties:
        The operation +, which we will call “prehend”, accepts two prehensions
            as arguments and produces a third prehension.
        Axioms:
            a.  Closure: Every prehending involving two prehensions will produce
                a prehension.
            b.  Associativity: (a + b) + c = a + (b + c)
            In a typical agent model, this will mean that we must ensure that,
                say, a neighborhood can interact with a neighborhood (b + c),
                and then with an agent (a + (b + c)). Furthermore, this must
                produce an identical prehension to that produced by an agent
                interacting with one neighborhood and then another one
                ((a + b) + c).
            c.  Identity: Any prehension prehending the null prehension produces
                unchanged.
            d.  Invertibility: For any prehension, there is another prehension
                that combines with it to produce the null prehension.
        The operation *, which we will call “intensify” (although it may also
            de-intensify) accepts an element of R and an element of G
            (a prehension), and produces an element of G.
        Axioms:
            a.  a, b member G:
                i.  (a + b)x = ax + bx
                ii. a(x + y) = ax + ay

    """

# we must pre-declare these, then use them, then init them at the bottom
#  of the file.
    X_PRE = None
    Y_PRE = None
    NULL_PRE = None
    NEUT_PRE = None

    @classmethod
    def from_vector(cls, v):
        """
        Convenience method to turn a vector into a prehension.
        """
        p = Prehension()
        p.vector = v
        return p

    def __init__(self, x=0, y=0):
        self.vector = np.array([x, y])

    def __str__(self):
        return ("x: %f, y: %f" % (self.vector[X], self.vector[Y]))

    def prehend(self, other):
        """
        In this class, a prehension prehends another prehension
        through vector addition.
        other: prehension to prehend
        """
        return Prehension.from_vector(self.vector + other.vector)

    def intensify(self, a):
        """
        Here this is scalar multiplication of a vector.
        a: scalar to multiply by.
        """
        return Prehension.from_vector(self.vector * a)

    def direction(self):
        """
        This gets us the orientation of the vector: x, y, or neutral.
        We use it, for instance, to set an agent's market stance to
        buy or sell.
        """
        if self.vector[X] > self.vector[Y]:
            return Prehension.X_PRE
        elif self.vector[X] < self.vector[Y]:
            return Prehension.Y_PRE
        else:
            return Prehension.NEUT_PRE

    def project(self, x_or_y):
        """
        Projects the vector onto the x or y axis.
        Pass in X or Y as declared above.
        """
        return self.vector[x_or_y]

    def equals(self, other):
        """
        For prehensions of the base type, they are equal
        when their vetors are equal.
        """
        return np.array_equal(self.vector, other.vector)

    def reverse(self):
        """
        Reverse the vector.
        Reflection across line y = x.
        """
        new_vec = np.array(np.flipud(self.vector))
        return Prehension.from_vector(new_vec)

    def normalize(self):
        """
        Return a normalized prehension.
        If we get the NULL prehension, just return it.
        """
        if self.equals(Prehension.NULL_PRE):
            return Prehension.NULL_PRE

        return Prehension.from_vector(self.vector / np.linalg.norm(self.vector))


# Now we actually initialize the prehensions we declared above.
#  This can't be done earlier, since Prehension was just defined.
Prehension.X_PRE = Prehension.from_vector(X_VEC)
Prehension.Y_PRE = Prehension.from_vector(Y_VEC)
Prehension.NULL_PRE = Prehension.from_vector(NULL_VEC)
Prehension.NEUT_PRE = Prehension.from_vector(NEUT_VEC)


def stance_pct_to_pre(pct, x_or_y):
    """
    pct is our % of the way to the y-axis from
    the x-axis around the unit circle. (If x_or_y == Y, it is the opposite.)
    It will return the x, y coordinates of the point that % of the way.
    I.e., .5 returns NEUT_VEC, 0 returns X_VEC.
    """
    if x_or_y == Y:
        pct = 1 - pct
    if pct == 0:
        return Prehension.X_PRE
    elif pct == .5:
        return Prehension.NEUT_PRE
    elif pct == 1:
        return Prehension.Y_PRE
    else:
        angle = 90 * pct
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        return Prehension(x, y)
