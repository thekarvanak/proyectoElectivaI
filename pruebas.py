def dec2bin(n):
    if n == 0:
        return '0'
    bin = ""
    while n > 0:
        bin += str(n % 2)
        n = n // 2

    return bin[::-1]


def bin2dec(b):
    b = b[::-1]
    r = 0
    for i in range(len(b)):
        r += int(b[i]) * 2**i
    return r


print(dec2bin(4))
print(dec2bin(5))
print(dec2bin(25))
print(bin2dec('100'))
print(bin2dec('101'))
print(bin2dec('11001'))
