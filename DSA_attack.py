import random
import string
import sympy
import math
from Crypto.Hash import SHA
import os
import olll


def parameters(p_length, q_length):
    stop = 2 ** 10
    while True:
        counter = 0
        q = sympy.randprime(2 ** (q_length - 1), 2 ** q_length - 1)
        while True:
            a = int((2 ** (p_length - 1)) / q)
            b = int((2 ** p_length - 1) / q)
            k = sympy.randprime(a, b) + 1
            p = k * q + 1
            counter += 1
            if (sympy.isprime(p)) or counter == stop:
                break
        if counter != stop:
            break
    return p, q


def mygma_keys(path, p, q, g):
    with open(path, 'w') as file:
        file.write("p: " + str(p) + "\n")
        file.write("q: " + str(q) + "\n")
        file.write("g: " + str(g) + "\n")
        file.close()


def random_string(string_length=10):
    letters = string.ascii_lowercase
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(string_length))


def params(path, p, q):
    a = (p - 1) // q
    # print("a: {}".format(a))
    h = random.randint(2, p - 2)
    # print("h: {}".format(h))
    g = pow(h, a, p)
    # print("g: {}".format(g))
    mygma_keys(path, p, q, g)
    return p, q, g


def key_pair_for_user(path, p, q, g):
    x = random.randint(1, q - 1)
    # print("x: {}".format(x))
    y = pow(g, x, p)
    # print("y: {}".format(y))
    with open(path, 'a') as file:
        file.write("x: " + str(x) + "\n")
        file.write("y: " + str(y) + "\n")
        file.close()
    return x, y


def sign(p, q, g, message, x):
    while True:
        k = random.randint(1, q - 1)
        if k.bit_length() == q.bit_length():
            break
    # print("k: {}".format(k))
    r = (pow(g, k, p)) % q
    u = SHA.new(message.encode("utf-8")).hexdigest()
    k_prim = pow(k, q - 2, q)
    h_m = int(u, 16)
    x_r = (x * r) % q
    s = (k_prim * (h_m + x_r)) % q
    return r, s, k


def verify(p, q, g, r, s, message, y):
    w = pow(s, q - 2, q)
    u = SHA.new(message.encode("utf-8")).hexdigest()
    h_m = int(u, 16)
    u1 = (h_m * w) % q
    u2 = (r * w) % q
    v1 = pow(g, u1, p)
    v2 = pow(y, u2, p)
    v3 = (v1 * v2) % p
    v = v3 % q
    if v == r:
        return True
    else:
        return False


# przygotowanie wynikow do pliku
def results_in_file(path, p, q, g, x, message_length, number_of_signatures):
    with open(path, 'w') as file:
        for i in range(number_of_signatures):
            message = random_string(math.floor(math.log(2 ** message_length, 10)))
            file.write(str(i) + " ")
            file.write(message + " ")
            r, s, k = sign(p, q, g, message, x)
            if r != 0 and s != 0:
                file.write(str(r) + " " + str(s) + " " + str(k) + "\n")
        file.close()


def attack(path_results, dimension, number_of_bits, q):
    mask = (1 << number_of_bits) - 1
    t = []
    u = []
    with open(path_results, 'r') as file:
        for line in file:
            tmp = line.split()
            s_prim = pow(int(tmp[3]), q - 2, q)
            # print("s_prim: {}".format(s_prim))
            rs_prim = (int(tmp[2]) * s_prim) % q
            # print("rs_prim: {}".format(rs_prim))
            # t.append(rs_prim)
            # print("result: {}".format(((rs_prim // (2 ** l)) % q)))
            a = int(tmp[4]) & mask
            # print("a: {}".format(str(a)))
            hash = SHA.new(tmp[1].encode("utf-8")).hexdigest()
            h_m = int(hash, 16)
            # h_m = int(tmp[1], 16)
            # print("h_m: {}".format(str(h_m)))
            hs = h_m * s_prim % q
            # print("hs: {}".format(str(hs)))
            u_prim = (a - hs) % q
            # print("u_prim: {}".format(str(u_prim)))
            tmp_t = ((rs_prim * (pow((pow(2, q - 2, q)), number_of_bits, q))) % q)
            tmp_u = ((u_prim * (pow((pow(2, q - 2, q)), number_of_bits, q))) % q)
            if tmp_t != 0 and tmp_u != 0:
                t.append(tmp_t)
                u.append(tmp_u)
            # u.append(u_prim)
            # print("u: {}".format(str(((u_prim // (2 ** l)) % q))))
        file.close()
    return t, u


def create_basis(t, u, dimension, number_of_bits, q):
    new_basic = []
    for i in range(dimension):
        tmp = []
        for j in range(dimension + 2):
            if i == j:
                tmp.append(q * (2 ** (number_of_bits + 1)))
            else:
                tmp.append(0)
        new_basic.append(tmp)
    tmp = []
    for i in range(dimension):
        tmp.append((2 ** (number_of_bits + 1)) * t[i])
    tmp.append(1)
    tmp.append(0)
    new_basic.append(tmp)
    tmp = []
    for i in range(dimension):
        tmp.append((2 ** (number_of_bits + 1)) * u[i])
    tmp.append(0)
    tmp.append(q)
    new_basic.append(tmp)
    # for i in range(dimension + 2):
    #     print(new_basic[i])
    return new_basic


def get_new_basic_lll(basic):
    print(basic)
    print("-"*60)
    reduced_basis = olll.reduction(basic, 0.75)
    print(reduced_basis)
    return reduced_basis


def find_second(output):
    sum = []
    for i in output:
        suma = 0
        for k in i:
            suma = suma + k * k
        sum.append(suma)
    index = list(range(0, len(sum)))
    zipped = list(zip(sum, index))
    # Printing zipped list
    print("Initial zipped list - ", str(zipped))
    # Using sorted and lambda
    res = sorted(zipped, key=lambda x: x[0])

    # printing result
    # print("final list - ", str(res))
    print("res:".format(res[1][1]))
    return res[1][1]


def get_secret_key(output, index, dimension, q):
    key_1 = output[index][dimension]
    key_2 = -(output[index][dimension] - q)
    key_3 = -output[index][dimension]
    key_4 = (output[index][dimension] + q)
    print("Mozliwe klucze to:\n")
    print("Klucz nr 1:\t {}\n".format(key_1))
    print("Klucz nr 2:\t {}\n".format(key_2))
    print("Klucz nr 3:\t {}\n".format(key_3))
    print("Klucz nr 4:\t {}\n".format(key_4))