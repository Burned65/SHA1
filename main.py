import hashlib


def pre_processing(m):
    len_m = len(m) * 8
    m += 0x80.to_bytes(1, 'big')
    while (len(m) * 8) % 512 != 448:
        m += bytearray(1)
    m += len_m.to_bytes(8, 'big')
    tmp = []
    tmp_bytes = bytearray()
    for i, item in enumerate(m):
        if (i * 8) // 512 == len(tmp):
            tmp_bytes += item.to_bytes(1, 'big')
        if len(tmp_bytes) == 512 // 8:
            tmp.append(tmp_bytes)
            tmp_bytes = bytearray()
    return tmp


def process_blocks(m):
    m = split_blocks(m)
    m = add_blocks(m)
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    for item in m:
        for i in range(80):
            if i <= 19:
                f = (b & c) | ((b ^ 0b11111111111111111111111111111111) & d)
                k = 0x5a827999
            elif i <= 39:
                f = b ^ c ^ d
                k = 0x6ed9eba1
            elif i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8f1bbcdc
            else:
                f = b ^ c ^ d
                k = 0xca62c1d6
            tmp = ((left_rotate(a, 5)) + f + e + k + item[i]) & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = tmp
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    h0 = h0.to_bytes(4, 'big')
    h1 = h1.to_bytes(4, 'big')
    h2 = h2.to_bytes(4, 'big')
    h3 = h3.to_bytes(4, 'big')
    h4 = h4.to_bytes(4, 'big')
    return h0 + h1 + h2 + h3 + h4


def left_rotate(item, rotations):
    rotations %= 32
    mask = int("1" * rotations, 2)
    mask <<= 32 - rotations
    mask &= item
    mask >>= 32 - rotations
    item <<= rotations
    item |= mask
    item &= 0xffffffff
    return item


def split_blocks(m):
    tmp = [[]] * len(m)
    for i, item in enumerate(m):
        for j in range(len(item) // 4):
            tmp[i].append(int(item[j*4:(j+1)*4].hex(), 16))
    return tmp


def add_blocks(m):
    for i, item in enumerate(m):
        for j in range(16, 80):
            tmp = left_rotate(item[j-3] ^ item[j-8] ^ item[j-14] ^ item[j-16], 1)
            m[i].append(tmp)
    return m


def sha1(m):
    return process_blocks(pre_processing(m))


if __name__ == '__main__':
    print(sha1("adadadadadadadadadadadadadadadadadadadadadadadadadadadada".encode()).hex())
    print(hashlib.sha1("adadadadadadadadadadadadadadadadadadadadadadadadadadadada".encode()).hexdigest())
