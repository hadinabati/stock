from cryptography.fernet import Fernet

from database import mongodb as db

collection = db.User_collection
secrect_key = b'V6xEjNgbCaihvY5q23F2hqbc4dY9CjAMtbeqHVdQzbs='


def hash_passing(passwords: str):
    f = Fernet(key=secrect_key)
    hash = f.encrypt(bytes(passwords, 'utf-8'))
    return hash.decode('utf-8')


def unhashing(passwords: str = ''):
    f = Fernet(secrect_key)
    decoded = f.decrypt(passwords.encode()).decode("utf-8")
    return decoded
