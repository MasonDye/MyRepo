import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key)
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key)
    print("密钥对已生成：private_key.pem 和 public_key.pem")

def sign_file(filename, private_key_path):
    with open(private_key_path, "rb") as private_file:
        private_key = RSA.import_key(private_file.read())
    with open(filename, "rb") as file:
        data = file.read()
    hashed_data = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(hashed_data)
    with open(filename + ".sig", "wb") as signature_file:
        signature_file.write(signature)
    print(f"文件 {filename} 已签名为 {filename}.sig")

def verify_signature(filename, public_key_path):
    with open(public_key_path, "rb") as public_file:
        public_key = RSA.import_key(public_file.read())
    with open(filename, "rb") as file:
        data = file.read()
    hashed_data = SHA256.new(data)
    with open(filename + ".sig", "rb") as signature_file:
        signature = signature_file.read()
    try:
        pkcs1_15.new(public_key).verify(hashed_data, signature)
        return True
    except (ValueError, TypeError):
        return False

def encrypt_file(filename, public_key_path):
    with open(public_key_path, "rb") as public_file:
        public_key = RSA.import_key(public_file.read())
    cipher = PKCS1_OAEP.new(public_key)
    with open(filename, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(filename + ".cy", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    print(f"文件 {filename} 已加密为 {filename}.cy")

def decrypt_file(filename, private_key_path):
    with open(private_key_path, "rb") as private_file:
        private_key = RSA.import_key(private_file.read())
    cipher = PKCS1_OAEP.new(private_key)
    with open(filename, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_filename = filename.replace(".cy", "")
    with open(decrypted_filename, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
    print(f"文件 {filename} 已解密为 {decrypted_filename}")

def main():
    while True:
        print("\n请选择操作：")
        print("1. 生成密钥对")
        print("2. 加密文件")
        print("3. 解密文件")
        print("4. 签名文件")
        print("5. 验证文件签名")
        print("6. 退出")
        choice = input("输入选项编号：")

        if choice == "1":
            generate_key_pair()
        elif choice == "2":
            filename = input("请输入要加密的文件名：")
            public_key_path = input("请输入公钥路径：")
            encrypt_file(filename, public_key_path)
        elif choice == "3":
            filename = input("请输入要解密的文件名：")
            private_key_path = input("请输入私钥路径：")
            decrypt_file(filename, private_key_path)
        elif choice == "4":
            filename = input("请输入要签名的文件名：")
            private_key_path = input("请输入私钥路径：")
            sign_file(filename, private_key_path)
        elif choice == "5":
            filename = input("请输入要验证签名的文件名：")
            public_key_path = input("请输入公钥路径：")
            if verify_signature(filename, public_key_path):
                print("签名验证通过")
            else:
                print("签名验证失败")
        elif choice == "6":
            print("退出程序")
            break
        else:
            print("无效的选项，请重新输入")

if __name__ == "__main__":
    main()
