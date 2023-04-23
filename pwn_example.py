from pwn import *

# Start the process
p = process('./safety_first')

# Wait for the prompt
p.recvuntil("""Welcome to my 🚀 BLAZING FAST 🚀 caesar cipher program.
Enter your input: """)

# Send the buffer
p.sendline('AAAAA')

# Print the response
print(p.recvall())
