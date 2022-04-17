import eel
from btc import *
from requests import *
import re

is_hex = True
is_big = True

eel.init("web")

def pub_to_address(B) -> str:
    return pubkey_to_address(B)

def pub_to_address_compressed(B) -> str:
    return pubkey_to_address(f"02{hex(B[0])[2:]}".encode("utf-8"))

def get_balance(address):
    url = f"https://blockchain.info/address/{address}?format=json"
    
    try: 
        balance = int(get(url).json()["final_balance"])
        if balance > 0:
            balance /= 100000000
        return balance 
    except:
        return "Error"

def get_int_from_another_type(key):
    if type(key) == int:
        return key

    if key[:2] == "0x":
        key = int(key,16)
    elif re.sub("[^0-9]", "", key) == key:
        key = int(key)
    else:
        key = int(sha256(key),16)

    return key

@eel.expose
def switch_curve():
    global is_big
    is_big = not is_big
    set_curve(is_big)
        
@eel.expose
def swith_format():
    global is_hex
    is_hex = not is_hex

@eel.expose
def set_curve(is_big):
    global N
    Edit(is_big)
    Edits(is_big)
    N = 115792089237316195423570985008687907852837564279074904382605163141518161494337 if is_big else 79
    
@eel.expose
def get_private_key_info(key, check_balance):
    if key == "":
        return ["","","","","","","",""]
    key = get_int_from_another_type(key)
    B = privkey_to_pubkey(key)
    key_dec = str(key)
    key_hex = hex(key)
    address_u = pub_to_address(B)
    address_c = pub_to_address_compressed(B)

    if check_balance:
        balance_u = get_balance(address_u)    
        balance_c = get_balance(address_c)    
    else:
        balance_u = ""
        balance_c = ""

    Bx = hex(B[0])
    By = hex(B[1])


    return [Bx,By, key_dec, key_hex, address_u, address_c, balance_c, balance_u]

@eel.expose
def get_rsz(x1,a1,b1):
    if "" in [x1,a1,b1]:
        return ["","","","",x1,a1,b1]

    if x1 == "-random":
        x1 = randint(1,N-1)
    elif "[" in x1 and "]" in x1:
        x1 = [get_int_from_another_type(i) for i in re.sub("[^a-z0-9]", " ",x1[1:-1]).split(" ")]
    else:
        x1 = get_int_from_another_type(x1)

    if a1 == "-random":
        a1 = randint(1,N-1)

    if b1 == "-random":
        b1 = randint(1,N-1)

    a1 = get_int_from_another_type(a1)
    b1 = get_int_from_another_type(b1)

    info = get_info_from_xab(x1, a1, b1)

    r1,s1,z1 = info["rsz"]
    r1 = r1[0]
    
    k1 = hex(info["k"]) if is_hex else str(info["k"]) if "k" in list(info.keys()) else ""
    
    if is_hex:
        r1,s1,z1,x1,a1,b1 = [hex(i) for i in [r1,s1,z1,x1,a1,b1]]
    else:
        r1,s1,z1,x1,a1,b1 = [str(i) for i in [r1,s1,z1,x1,a1,b1]]

    return [r1,s1,z1,k1,x1,a1,b1]

@eel.expose
def calc(data):
    
    x1 = data["x1"]
    x2 = data["x2"]
    x3 = data["x3"]
    x4 = data["x4"]
    
    if x1 != "":
        if "[" in x1 and "]" in x1:
            x1 = [get_int_from_another_type(i) for i in re.sub("[^a-z0-9]", " ",x1[1:-1]).split(" ")]
        else:
            x1 = get_int_from_another_type(x1)

    if x2 != "":
        if "[" in x2 and "]" in x2:
            x2 = [get_int_from_another_type(i) for i in re.sub("[^a-z0-9]", " ",x2[2:-2]).split(" ")]
        else:
            x2 = get_int_from_another_type(x2)

    if x3 != "":
        if "[" in x3 and "]" in x3:
            x3 = [get_int_from_another_type(i) for i in re.sub("[^a-z0-9]", " ",x3[3:-3]).split(" ")]
        else:
            x3 = get_int_from_another_type(x3)

    if x4 != "":
        if "[" in x4 and "]" in x4:
            x4 = [get_int_from_another_type(i) for i in re.sub("[^a-z0-9]", " ",x4[4:-4]).split(" ")]
        else:
            x4 = get_int_from_another_type(x4)

    if x1 != "":
        a1 = get_int_from_another_type(data["a1"]); b1 = get_int_from_another_type(data["b1"])
        r1 = get_int_from_another_type(data["r1"]); s1 = get_int_from_another_type(data["s1"])
        z1 = get_int_from_another_type(data["z1"]); k1 = get_int_from_another_type(data["k1"])

    if x2 != "":
        a2 = get_int_from_another_type(data["a2"]); b2 = get_int_from_another_type(data["b2"])
        r2 = get_int_from_another_type(data["r2"]); s2 = get_int_from_another_type(data["s2"])
        z2 = get_int_from_another_type(data["z2"]); k2 = get_int_from_another_type(data["k2"])

    if x3 != "":
        a3 = get_int_from_another_type(data["a3"]); b3 = get_int_from_another_type(data["b3"])
        r3 = get_int_from_another_type(data["r3"]); s3 = get_int_from_another_type(data["s3"])
        z3 = get_int_from_another_type(data["z3"]); k3 = get_int_from_another_type(data["k3"])

    if x4 != "":    
        a4 = get_int_from_another_type(data["a4"]); b4 = get_int_from_another_type(data["b4"])
        r4 = get_int_from_another_type(data["r4"]); s4 = get_int_from_another_type(data["s4"])
        z4 = get_int_from_another_type(data["z4"]); k4 = get_int_from_another_type(data["k4"])

    result = eval(data["task"]) % N

    return [hex(result), str(result)]

@eel.expose
def get_pub_from_rsz(r1,s1,z1):

    r1,s1,z1 = [get_int_from_another_type(i) for i in [r1,s1,z1]]
    
    info = get_B_from_rsz(r1,s1,z1)

    print(info)

eel.start("index.html",size=(1920,1080), port=8080)
