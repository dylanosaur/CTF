import base64
def brute_force_b64(x):
    decoded = ""
    for i in range(3):
        try:
            decoded = base64.b64decode(x + '=' * i).decode('ascii', errors='ignore')
            break
        except Exception as ex:
            pass
    return decoded
