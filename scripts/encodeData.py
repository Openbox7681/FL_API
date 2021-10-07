from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# 要加密的資料（必須為 bytes）
data = b'My secret data.'

# 讀取 RSA 公鑰
publicKey = RSA.import_key(open("public.pem").read())

# 建立隨機的 AES Session 金鑰
sessionKey = get_random_bytes(16)

# 以 RSA 金鑰加密 Session 金鑰
cipherRSA = PKCS1_OAEP.new(publicKey)
encSessionKey = cipherRSA.encrypt(sessionKey)

# 以 AES Session 金鑰加密資料
cipherAES = AES.new(sessionKey, AES.MODE_EAX)
ciphertext, tag = cipherAES.encrypt_and_digest(data)

print(encSessionKey)
print(cipherAES.nonce)
print(tag)
print(ciphertext)

# 將加密結果寫入檔案
with open("encrypted_data.bin", "wb") as f:
    f.write(encSessionKey)
    f.write(cipherAES.nonce)
    f.write(tag)
    f.write(ciphertext)
