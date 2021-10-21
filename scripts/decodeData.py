from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

# 讀取 RSA 私鑰
privateKey = RSA.import_key(open("private.pem").read())

# 從檔案讀取加密資料
with open("encrypted_data.bin", "rb") as f:
    encSessionKey = f.read(privateKey.size_in_bytes())
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read(-1)

print(encSessionKey)
print(nonce)
print(tag)
print(ciphertext)


# 以 RSA 金鑰解密 Session 金鑰
cipherRSA = PKCS1_OAEP.new(privateKey)
sessionKey = cipherRSA.decrypt(encSessionKey)

# 以 AES Session 金鑰解密資料
cipherAES = AES.new(sessionKey, AES.MODE_EAX, nonce)
data = cipherAES.decrypt_and_verify(ciphertext, tag)

# 輸出解密後的資料
print(data.decode("utf-8"))