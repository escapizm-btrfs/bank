from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher



password_context = PasswordHash(hashers=[BcryptHasher()])

def hash_password(password:str):
    password_hash = password_context.hash(password)
    return password_hash

def verify_password(plain_pass:str, hash_pass:str):
    verify_result = password_context.verify(plain_pass, hash_pass)
    return verify_result

'''def random_account_number():
    lst = []
    for _ in range(16):
        num = random.randint(0, 9)
        lst.append(num)
    return lst'''