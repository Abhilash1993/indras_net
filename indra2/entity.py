"""
This file defines an Entity.
"""
import numpy as np
import json
from random import uniform
from collections import OrderedDict

LOW_RAND = .666
HI_RAND = 1.5

empty_dict = OrderedDict()


def type_hash(ent):
    """
    type_hash() will return an ID that identifies
    the ABM type of an entity.
    """
    return len(ent)  # temp solution!


class Entity(object):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """

    def __init__(self, name, attrs=empty_dict):
        self.name = name
        self.attrs = OrderedDict()
        for i, (k, v) in enumerate(attrs.items()):
            self.attrs[k] = i  # store index into np.array!
        self.val_vect = np.array(list(attrs.values()))
        self.type_sig = type_hash(self)

    def __eq__(self, other):
        if self.type_sig != other.type_sig:
            return False
        else:
            return np.array_equal(self.val_vect, other.val_vect)

    def __str__(self):
        return self.name

    def __repr__(self):
        return json.dumps(self.to_json())

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.val_vect[self.attrs[key]]

    def __setitem__(self, key, value):
        if key not in self.attrs:
            raise KeyError(key)
        self.val_vect[self.attrs[key]] = value

    def __contains__(self, item):
        return item in self.attrs

    def __iter__(self):
        return iter(self.attrs)

    def __reversed__(self):
        return reversed(self.attrs)

    def __call__(self):
        """
        Entities will 'act' by being called as a function.
        We are just going to randomly alter the vector
        in the base class, to make sure something happens!
        """
        print(self.name + " is acting!")
        self *= uniform(LOW_RAND, HI_RAND)

    def __iadd__(self, scalar):
        self.val_vect += scalar
        return self

    def __isub__(self, scalar):
        self.val_vect -= scalar
        return self

    def __imul__(self, scalar):
        self.val_vect *= scalar
        return self

# numpy doesn't implement this! must investigage.
#    def __idiv__(self, scalar):
#        self.val_vect /= scalar
#        return self

    def magnitude(self):
        return np.linalg.norm(self.val_vect)

    def sum(self):
        return self.val_vect.sum()

    def attrs_to_dict(self):
        d = OrderedDict()
        for key in self.attrs:
            d[key] = self[key]
        return d

    def same_type(self, other):
        return self.type_sig == other.type_sig

    def to_json(self):
        return {"name": self.name, "attrs": self.attrs_to_dict()}
