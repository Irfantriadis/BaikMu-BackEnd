import hashlib

password = ''
password_hashed = hashlib.sha256(password.encode()).hexdigest()
print(password_hashed)