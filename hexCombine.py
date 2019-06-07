import random

import itertools


class Rotation:
    def __init__(self, axis=0):
        self.axis = axis


class Cut:
    def __init__(self, x, y, z):
        self.xyz = (x, y, z)

    def __lt__(self, other):
        if self.xyz[0] < other.xyz[0] : return True
        if self.xyz[1] < other.xyz[1]: return True
        if self.xyz[2] < other.xyz[2]: return True
        return False

    def rotate(self, axis , reverse = False ):
        if reverse == False:
            if axis == 2:
                    return Cut( self.xyz[1], -self.xyz[0], self.xyz[2])
            if axis == 1:
                    return Cut( self.xyz[2], self.xyz[1], -self.xyz[0])
            if axis == 0:
                    return Cut(self.xyz[0], self.xyz[2], -self.xyz[1])
        else:
            if axis == 2:
               return Cut(-self.xyz[1], self.xyz[0], self.xyz[2])
            if axis == 1:
                return Cut(-self.xyz[2], self.xyz[1], self.xyz[0])
            if axis == 0:
                return Cut(self.xyz[0], -self.xyz[2], self.xyz[1])



    def mirror(self, axis):
        if axis == 0:
            return Cut( -self.xyz[0], self.xyz[1], self.xyz[2])
        if axis == 1:
                return Cut( self.xyz[0], -self.xyz[1], self.xyz[2])
        if axis == 2:
                return Cut( self.xyz[0], self.xyz[1], -self.xyz[2])

    def __repr__(self):
        return "Cut(" + str(self.xyz) +") "

    def __eq__(self, s):
        if abs(self.xyz[0] - s.xyz[0]) < 0.01:
            if abs(self.xyz[0] - s.xyz[0]) < 0.01:
                if abs(self.xyz[0] - s.xyz[0]) < 0.01:
                    return True
        return False





cutPoints_x = Cut(0, -1, -1), Cut(0, 1, -1), Cut(0, -1, 1), Cut(0, 1, 1)
cutPoints_y = Cut(-1, 0, -1), Cut(1, 0, -1), Cut(-1, 0, 1), Cut(1, 0, 1)
cutPoints_z = Cut(-1, -1, 0), Cut(1, -1, 0), Cut(-1, 1, 0), Cut(1, 1, 0)

cutPoints = cutPoints_x + cutPoints_y + cutPoints_z
print(cutPoints)


class Hexa:
    def __init__(self, cuts):
        self.cuts = sorted(cuts )
    def __repr__(self):
        return "Hexa("+str(self.cuts)+")"

    def rotate(self,axis,reverse = False ):
        return Hexa(  [c.rotate(axis,reverse) for c in self.cuts]  )
    def mirror(self, axis):
         return Hexa([c.mirror(axis) for c in self.cuts])

    def __eq__(self, other):
        if len(self.cuts) != len(other.cuts): return False
        for i in range(len(self.cuts)):
            if self.cuts[i] != other.cuts[i]: return False
        return True



def convertH( H , c1,c2 ):
    print( H,c1,c2)
    if (c1 == c2) :
        return H
    for axis in range(3):
        if c1.rotate( axis ) == c2 :
           return  convertH(H.rotate(axis), c1.rotate(axis), c2)
        if c1.rotate(axis,reverse = True  ) == c2:
           return convertH(H.rotate(axis,reverse = True ), c1.rotate(axis,reverse = True ), c2)

    for axis in range(3):
       if (c1.xyz[axis] != 0 ):
          if c1.xyz[axis] == -c2.xyz[axis]:
             return convertH(H.mirror(axis), c1.mirror(axis)  ,c2)

    return H

def apply_t(H,x):
    if (x == "rx"): return H.rotate(0)
    if (x == "ry"): return H.rotate(1)
    if (x == "rz"): return H.rotate(2)
    if (x == "mx"): return H.mirror(0)
    if (x == "my"): return H.mirror(1)
    if (x == "mz"): return H.mirror(2)
    raise " ??"

def apply_acc(h1, tr):
    if (len(tr) == 0  ):
        return h1
    return apply_acc( apply_t(h1, tr[0]) , tr[1:])


def apply_until_equals(h1, h2, tr, acc=None):
    if acc is None:
        acc = []
    if tr ==[]: return False,[]
    if h1 == h2: return True,acc
    tr_nex = []
    if len(tr) > 1 : tr_nex=  tr[1:]
    return apply_until_equals(apply_t(h1,tr[0]),h2, tr_nex , acc+[tr[0]] )



smm = "rx rx rx ry ry ry rz rz rz mx my mz".split(" ")



t_perm = itertools.permutations(smm, 7)
for p in t_perm:
    print(p)
    break

perm = itertools.combinations(cutPoints,3)


htest = Hexa([Cut(1, -1, 0), Cut(1, 1, 0),Cut(1, 0, -1) ])
for p in perm:
  h1 =  Hexa( p[0:3] )
  print(h1)
  for pr in t_perm:
     q , acc = apply_until_equals( h1, htest,  pr)
     #print(h1, htest, q, pr )
     if q:
         print(apply_acc(h1,acc))
