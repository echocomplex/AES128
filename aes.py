"""

AES-128 CRYPTO
Creator - echo complex

"""

""" IMPORTS """
import numpy as np;


class AES128Error (Exception):
    def __init__ (self, text: str) -> None:
        self.text: str = text;



class AES128:
    def __init__ (self, key: str) -> None:
        if (len(key) != 16):
            raise AES128Error("Key must be 16 characters only.");
        self.__keys: tuple = ();
        self.__create_keys(self.__text_to_uni(key));
        self.__s_box = np.load('Lookup Tables/s_box.npy');
        self.__inv_s_box = np.load('Lookup Tables/inv_s_box.npy');

    def __create_keys (self, key: np.reshape) -> None:
        keys: list = [key];
        rcon: list = [1, 0, 0, 0];
        for _ in range(10):
            matrix = keys[-1];
            new_matrix = np.zeros((4, 4), dtype=int);
            s_box = np.load('Lookup Tables/s_box.npy');
            for row in range(4):
                for col in range(4):
                    sub_row, sub_col = matrix[row, col]//16, matrix[row, col]%16;
                    new_matrix[row, col] = s_box[sub_row, sub_col];
            del s_box;
            rotated: tuple = (new_matrix[0, 1], new_matrix[0, 2], new_matrix[0, 3], new_matrix[1, 0],
                              new_matrix[1, 1], new_matrix[1, 2], new_matrix[1, 3], new_matrix[2, 0],
                              new_matrix[2, 1], new_matrix[2, 2], new_matrix[2, 3], new_matrix[3, 0],
                              new_matrix[3, 1], new_matrix[3, 2], new_matrix[3, 3], new_matrix[0, 0]);
            XORed = [];
            for y in range(0, 16, 4):
                xor = np.bitwise_xor((rotated[y], rotated[y+1], rotated[y+2], rotated[y+3]), rcon);
                XORed.append(xor[0]);
                XORed.append(xor[1]);
                XORed.append(xor[2]);
                XORed.append(xor[3]);
            final_matrix = np.reshape(XORed, (4, 4));
            keys.append(final_matrix);
        self.__keys: tuple = tuple(keys);

    @staticmethod
    def __text_to_uni (text: str) -> np.reshape:
        matrix = np.zeros(16, dtype=int);
        for i in range(16):
            matrix[i] = ord(text[i]);
        matrix = np.reshape(matrix, (4, 4));
        return matrix;

    @staticmethod
    def __back_to_str (matrix: np.array) -> str:
        flat = matrix.flatten();
        text: str = "";
        for i in range(16):
            text += chr(int(flat[i]));
        del flat;
        return text;

    def __AddRoundKey (self, matrix: np.reshape, key_index: int) -> np.reshape:
        with_round_key = np.bitwise_xor(matrix, self.__keys[key_index]);
        return with_round_key;

    def __SubBytes (self, matrix: np.reshape) -> np.reshape:
        with_SB = np.zeros((4, 4), dtype=int);
        for row in range(4):
            for col in range(4):
                sub_row, sub_col = matrix[row, col]//16, matrix[row, col]%16;
                with_SB[row, col] = self.__s_box[sub_row, sub_col];
        return with_SB;

    def __invSubBytes (self, matrix: np.reshape) -> np.reshape:
        with_SB = np.zeros((4, 4), dtype=int);
        for row in range(4):
            for col in range(4):
                sub_row, sub_col = matrix[row, col]//16, matrix[row, col]%16;
                with_SB[row, col] = self.__inv_s_box[sub_row, sub_col];
        return with_SB;

    @staticmethod
    def __ShiftRows (matrix: np.reshape) -> np.reshape:
        with_SR = np.zeros((4, 4), dtype=int);
        with_SR[0, 0], with_SR[0, 1], with_SR[0, 2], with_SR[0, 3] = matrix[0, 0], matrix[0, 1], matrix[0, 2], matrix[0, 3];
        with_SR[1, 0], with_SR[1, 1], with_SR[1, 2], with_SR[1, 3] = matrix[1, 1], matrix[1, 2], matrix[1, 3], matrix[1, 0];
        with_SR[2, 0], with_SR[2, 1], with_SR[2, 2], with_SR[2, 3] = matrix[2, 2], matrix[2, 3], matrix[2, 0], matrix[2, 1];
        with_SR[3, 0], with_SR[3, 1], with_SR[3, 2], with_SR[3, 3] = matrix[3, 3], matrix[3, 0], matrix[3, 1], matrix[3, 2];
        return with_SR;

    @staticmethod
    def __invShiftRows(matrix: np.reshape) -> np.reshape:
        with_SR = np.zeros((4, 4), dtype=int);
        with_SR[0, 0], with_SR[0, 1], with_SR[0, 2], with_SR[0, 3] = matrix[0, 0], matrix[0, 1], matrix[0, 2], matrix[0, 3];
        with_SR[1, 1], with_SR[1, 2], with_SR[1, 3], with_SR[1, 0] = matrix[1, 0], matrix[1, 1], matrix[1, 2], matrix[1, 3];
        with_SR[2, 2], with_SR[2, 3], with_SR[2, 0], with_SR[2, 1] = matrix[2, 0], matrix[2, 1], matrix[2, 2], matrix[2, 3];
        with_SR[3, 3], with_SR[3, 0], with_SR[3, 1], with_SR[3, 2] = matrix[3, 0], matrix[3, 1], matrix[3, 2], matrix[3, 3];
        return with_SR;

    @staticmethod
    def __MixColumns (matrix: np.reshape) -> np.reshape:
        def galois_multiplication (a: int, b: int) -> int:
            result: int = 0;
            for _ in range(8):
                if b & 1:
                    result ^= a;
                b >>= 1;
                if a & 0x80:
                    a = (a << 1) ^ 0x1B;
                else:
                    a <<= 1;
            return result;
        newarr = matrix.flatten();
        result = [0] * 4;
        for i in range(4):
            # polinomes
            result[i] = (
                    galois_multiplication(newarr[i], 0x02) ^
                    galois_multiplication(newarr[(i + 1) % 4], 0x03) ^
                    newarr[(i + 2) % 4] ^
                    newarr[(i + 3) % 4]
            );
        matrix_to_return = np.reshape(newarr, (4, 4));
        return matrix_to_return;

    def encrypt (self, text: str) -> str:
        splitted: list = [text[x:x+16] for x in range (0, len(text), 16)];
        if (len(text)%16 != 0):
            splitted[-1] = f"{splitted[-1]}{' '*(16-len(splitted[-1]))}";

        encrypted: str = "";
        for sub_string in splitted:
            uni_string = self.__text_to_uni(sub_string);
            to_next_step = self.__AddRoundKey(uni_string, 0);
            for i in range(1, 10):
                SubBytes = self.__SubBytes(to_next_step);
                ShiftRows = self.__ShiftRows(SubBytes);
                MixColumns = self.__MixColumns(ShiftRows);
                AddRoundKey = self.__AddRoundKey(MixColumns, i);
                to_next_step = AddRoundKey;
            SubBytes = self.__SubBytes(to_next_step);
            ShiftRows = self.__ShiftRows(SubBytes);
            AddRoundKey = self.__AddRoundKey(ShiftRows, 10);
            encrypted16: str = self.__back_to_str(AddRoundKey);
            encrypted += encrypted16;
        return encrypted;


    def decrypt (self, text: str) -> str:
        splitted: list = [text[x:x + 16] for x in range(0, len(text), 16)];
        if (len(text) % 16 != 0):
            splitted[-1] = f"{splitted[-1]}{' ' * (16 - len(splitted[-1]))}";

        decrypted: str = "";
        for sub_string in splitted:
            uni_string = self.__text_to_uni(sub_string);
            AddRoundKey = self.__AddRoundKey(uni_string, 10);
            ShiftRows = self.__invShiftRows(AddRoundKey);
            to_next_step = self.__invSubBytes(ShiftRows);
            for i in range(9, 0, -1):
                AddRoundKey = self.__AddRoundKey(to_next_step, i);
                MixColumns = self.__MixColumns(AddRoundKey);
                ShiftRows = self.__invShiftRows(MixColumns);
                SubBytes = self.__invSubBytes(ShiftRows);
                to_next_step = SubBytes;
            AddRoundKey = self.__AddRoundKey(to_next_step, 0);
            decrypted16: str = self.__back_to_str(AddRoundKey);
            decrypted += decrypted16;
        return decrypted;

    def encrypt_file (self, filename: str, text: str) -> None:
        encrypted: str = self.encrypt(text);
        with open(filename, "w") as f:
            f.write(encrypted);

    def decrypt_file (self, file) -> str:
        read = file.read();
        decrypted: str = self.decrypt(read);
        return decrypted;
