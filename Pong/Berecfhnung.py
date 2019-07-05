from math import atan, tan

a = 0.001

def Berechnung(m, xsp):
    mtangente=2*a*xsp
    ml = -1/mtangente
    BETA=atan(ml)
    ALPHA = atan(m)
    GAMMA = ALPHA-BETA
    GAMMASTRICH = BETA-GAMMA
    mn = tan(GAMMASTRICH)
    print(mn)

Berechnung(2,150)