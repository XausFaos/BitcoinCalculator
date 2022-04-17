from bitcoin import *
from random import randint

def Edits(big):
    if(big):
        global P,N,G
        
        P = 2**256 - 2**32 - 977
        N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        G = (Gx, Gy)

    else:
        G = (2,22)
        P = 67
        N = 79

def GetABFromRSZ(r, s, z, B):

    assert VerifiRSZ(r, s, z, B) == True, "Signature Is Not Valid"

    a = r * inv(s, N) % N
    b = z * inv(s, N) % N

    return (a, b)


def GetRSZwithAB(a, b, B):

    aB = fast_multiply(B, a)
    bG = fast_multiply(G, b)

    r = fast_add(aB, bG)
    s = r[0] * inv(a, N) % N
    z = b * s % N

    return ([r[0], r[1]], s, z)


def GetPrivateKeyFromDoubleR(r, s1, z1, s2, z2):

    k = (((z1-z2) * inv((s1-s2), N)) % N)
    x = (k * s1 - z1) * inv(r, N) % N

    return x


def VerifiRSZ(r, s, z, B):

    GmulZ = fast_multiply(G, z * inv(s, N))
    BmulS = fast_multiply(B, r * inv(s, N))
    Summ = fast_add(GmulZ, BmulS)[0] % N

    if(Summ == r):
        return True
    
    return False


def GetK(r, s, z, x):

    #assert VerifiRSZ(r, s, z, privkey_to_pubkey(x)) == True, "Sig not verifi"

    try:
        one = (x * r + z) % N
        k = one * inv(s, N) % N
        return k

    except:
        return "ZeroError"


def GetXWithRSZK(r, s, z, k):

    return ((k * s - z) * inv(r, N)) % N