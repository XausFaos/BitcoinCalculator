from random import randint
from bitcoinlibs.main import *

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

def get_ab_from_rsz(r, s, z, B):

    assert verifi_rsz(r, s, z, B) == True, "Signature Is Not Valid"

    a = r * inv(s, N) % N
    b = z * inv(s, N) % N

    return (a, b)

def get_info_from_xab(x, a1, b1):

    if(type(x) != int):
        r1, s1, z1 = get_rsz_with_ab(a1, b1, x)
        return {"rsz": [r1, s1, z1],
                "ab": [a1, b1],
                "B": x}

    B = privkey_to_pubkey(x)
    r1, s1, z1 = get_rsz_with_ab(a1, b1, B)
    k = get_k_from_rszx(r1[0], s1, z1, x)

    return {"rsz": [r1, s1, z1],
            "k": k,
            "ab": [a1, b1],
            "B": B,
            "x": x}

def get_random_x(count=1):
    return [randint(1, N - 1) for i in range(count)]

def get_pub_key(lst):
    return [privkey_to_pubkey(i) for i in lst]

def get_double_r(x1, x2=None, a1=randint(1, N-1), b1=randint(1, N-1), a2=randint(1, N-1)):

    if(x2 == None):
        x2 = x1

    b2 = (b1 + (N - (x2 * (a2 - a1))) - a1 * (x2-x1)) % N

    data1 = get_info_from_xab(x1, a1, b1)
    data2 = get_info_from_xab(x2, a2, b2)

    r1, s1, z1, k1 = data1["rsz"][0], data1["rsz"][1], data1["rsz"][2], data1["k"]
    r2, s2, z2, k2 = data2["rsz"][0], data2["rsz"][1], data2["rsz"][2], data2["k"]

    return {"ab": [[a1, b1], [a2, b2]],
            "rsz": [[r1, s1, z1], [r2, s2, z2]],
            "k": [k1, k2]}

def get_private_key_from_double_r(r, s1, z1, s2, z2):

    k = (((z1-z2) * inv((s1-s2), N)) % N)
    x = (k * s1 - z1) * inv(r, N) % N

    return x

def get_x_with_rsz_k(r, s, z, k):

    return ((k * s - z) * inv(r, N)) % N

def get_k_from_rszx(r, s, z, x):

    assert verifi_rsz(r, s, z, privkey_to_pubkey(x)) == True, "Sig not verifi"

    try:
        one = (x * r + z) % N
        k = one * inv(s, N) % N
        return k

    except:
        return "ZeroError"

def get_rsz_with_ab(a, b, B):

    aB = fast_multiply(B, a)
    bG = fast_multiply(G, b)

    r = fast_add(aB, bG)
    s = r[0] * inv(a, N) % N
    z = b * s % N

    return ([r[0], r[1]], s, z)

def verifi_rsz(r, s, z, B):

    GmulZ = fast_multiply(G, z * inv(s, N))
    BmulS = fast_multiply(B, r * inv(s, N))
    Summ = fast_add(GmulZ, BmulS)[0] % N

    if(Summ == r):
        return True
    
    return False

def get_next_B(B):
    return fast_add(B,G)

def subtraction(B1, B2):
    return fast_add(B1,[B2[0], -B2[1] % P])

def get_double_r_from_random_address(B1,a1=randint(1,N-1),b1=randint(1,N-1),s2 = randint(1,N - 1), z2 = randint(1,N - 1)):

    r1,s1,z1 = get_info_from_xab(B1,a1,b1)["rsz"]

    B2 = get_B_from_rsz(r1,s2,z2)

    a2,b2 = get_ab_from_rsz(r1[0],s2,z2,B2)

    r2,s2,z2 = get_info_from_xab(B2,a2,b2)["rsz"]

    return {"ab" : [a2,b2], 
            "rsz" : [r2,s2,z2],
            "B2" : B2,
            "B1" : B1}

def get_B_from_rsz(r,s,z):
    return subtraction(fast_multiply(r, s * inv(r[0],N)), fast_multiply(G, z * inv(r[0],N)))
