from aes import AES128;

if (__name__ == "__main__"):
    # TEXT ENCRYPTION AND DECRYPTION
    text: str = input("Enter text to encrypt >>> ");
    key: str = input("Enter key (16 chr) >>> ");
    print("\nEncrypting...\n");
    aes = AES128(key);
    enc = aes.encrypt(text);
    print(f"Your encrypted text: {enc}\n");
    print("Decrypting...\n");
    dec = aes.decrypt(enc);
    print(f"Your start text: {dec}");

    # FILE ENCRYPTION
    # text: str = input("Enter text to encrypt >>> ");
    # key: str = input("Enter key (16 chr) >>> ");
    # filename: str = input("Enter filename (without .txt) >>> ");
    # print("\nEncrypting...\n");
    # aes = AES128(key);
    # aes.encrypt_file(f"{filename}.txt", text);
    # print("File encrypted!");


    # FILE DECRYPTION
    # filename: str = input("Enter filename to decrypt (without .txt) >>> ");
    # key: str = input("Enter key (16 chr) >>> ");
    # print("\nDecrypting...\n");
    # aes = AES128(key);
    # decrypted = aes.decrypt_file(open(f"{filename}.txt", 'r'));
    # print(f"Decrypted text: {decrypted}");
