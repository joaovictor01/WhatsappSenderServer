import hashlib
import os
from base64 import b64decode, b64encode

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from passlib.hash import pbkdf2_sha256

ENCRYPTION_KEY = os.environ.get("SECRET_KEY")


def pad(s):
    block_size = 16
    remainder = len(s) % block_size
    padding_needed = block_size - remainder
    return s + padding_needed * " "


def unpad(s):
    return s.rstrip()


def encrypt(plain_text):
    # Gera um salt aleatório
    salt = get_random_bytes(AES.block_size)

    # Usa o Scrypt KDF para obter uma chave privada da chave secreta setada na
    # variável de ambiente
    private_key = hashlib.scrypt(
        ENCRYPTION_KEY.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    # Cria um cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # retorna um dicionário com o texto encriptado
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, "utf-8"))
    return {
        "cipher_text": b64encode(cipher_text).decode("utf-8"),
        "salt": b64encode(salt).decode("utf-8"),
        "nonce": b64encode(cipher_config.nonce).decode("utf-8"),
        "tag": b64encode(tag).decode("utf-8"),
    }


def decrypt(enc_dict):
    # Decodifica as entradas em base 64 do dicionário
    salt = b64decode(enc_dict["salt"])
    cipher_text = b64decode(enc_dict["cipher_text"])
    nonce = b64decode(enc_dict["nonce"])
    tag = b64decode(enc_dict["tag"])

    # Gera uma chave privada a partir da chave secreta e do salt
    private_key = hashlib.scrypt(
        ENCRYPTION_KEY.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32
    )

    # Cria a configuração do cipher
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # Decripta o texto do cipher
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    # Retorna o resultado decriptado
    return bytes.decode(decrypted)


def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, hash: str):
    return pbkdf2_sha256.verify(password, hash)
