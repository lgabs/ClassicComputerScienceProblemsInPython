from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    # generate length random bytes
    tb: bytes = token_bytes(length)
    # convert those bytes into a bit string and return it
    return int.from_bytes(tb, "big")

def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy  # XOR
    return dummy, encrypted

def decrypt(encrypted: int, dummy: str):
    decrypted_int: int = encrypted ^ dummy  # XOR
    decrypted_bytes: bytes = decrypted_int.to_bytes(length=(decrypted_int.bit_length()+ 7) // 8, byteorder="big")
    decrypted_str: str = decrypted_bytes.decode()
    return decrypted_str

if __name__ == "__main__":
    s = "One Time Pad!"
    key1, key2 = encrypt(s)
    result: str = decrypt(key1, key2)
    print(f"to encript: '{s}'\ndecrypted: '{result}'")