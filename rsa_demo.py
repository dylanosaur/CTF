# first ill forward sim my algorithm

def bytes_to_integer(data):
    output = 0    
    size = len(data)
    for index in range(size):
        output |= data[index] << (8 * (size - 1 - index))
    return output

def integer_to_bytes(integer, _bytes):
    output = bytearray()
    for byte in range(_bytes):        
        output.append((integer >> (8 * (_bytes - 1 - byte))) & 255)
    return output


fake_flag = 'abc'

fake_bytes = bytearray(fake_flag, encoding='ascii')
# choose p,q
p = 7883
q = 7907
n = p*q
# choose e
e = 3
# calculate d
d = 41543395


fake_cipher = bytes_to_integer(fake_bytes)
print('starting M', fake_cipher)

c = (fake_cipher**e)%n
fake_c = c
print('encoded', c)
    

M = pow(c, d, n)
print('result', M)
print(integer_to_bytes(M,30).decode())


# now apply the method to the problem at hand

n = 10888751337932558679268839254528888070769213269691871364279830513893837690735136476085167796992556016532860022833558342573454036339582519895539110327482234861870963870144864609120375793020750736090740376786289878349313047032806974605398302398698622431086259032473375162446051603492310000290666366063094482985737032132318650015539702912720882013509099961316767073167848437729826084449943115059234376990825162006299979071912964494228966947974497569783878833130690399504361180345909411669130822346252539746722020515514544334793717997364522192699435604525968953070151642912274210943050922313389271251805397541777241902027
e = 3
c = 2449457955338174702664398437699732241330055959255401949300755756893329242892325068765174475595370736008843435168081093064803408113260941928784442707977000585466461075146434876354981528996602615111767938231799146073229307631775810351487333


# in this case we know that the message is quite small, and M**e  << n, so that we can calcuate d directly as 1/e
# however we must be careful to not truncate with floating point precision, so we need an efficient way of computing M**(1/3)

print(pow(fake_c, e) < n)
M = pow(c, 1/e)
print(M)

def find_invpow(x,n):
    """Finds the integer component of the n'th root of x,
    an integer such that y ** n <= x < (y + 1) ** n.
    """
    high = 1
    while high ** n <= x:
        high *= 2
    low = high//2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1




m2 = find_invpow(c, e)
print(m2)
# print(int(M), int(M+1), int(M-1))
print(integer_to_bytes(m2, 40).decode())
