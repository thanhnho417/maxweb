import random, string, json
def randomcode(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


while True:
    n = int(input('Nhập dãy số mã hóa: '))
    if n == 0: exit()
    print(randomcode(n))

