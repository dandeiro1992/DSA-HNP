from sage.all import *

F =GF(2)
print(F)

R = PolynomialRing( F, name='X' )
print (R)

G = GL(3,F)
print (G.order())

E = EllipticCurve( GF(2**53), [1,0,0,0,1] )
print ("ORDER %s for %s" % ( E.order().factor(), E ))