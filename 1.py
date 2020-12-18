import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
backend = default_backend()
key = os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()
ct = encryptor.update(b"a secret message") + encryptor.finalize()
decryptor = cipher.decryptor()
text = decryptor.update(ct) + decryptor.finalize()
print(encryptor);
print(text);


def file_decrypt(key, iv, fileinpath, fileoutpath):
    backend = default_backend();
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
    decryptor = cipher.decryptor();
    block = 31;
    filein = open(fileinpath, "rb");
    fileout = open(fileoutpath, "wb");
    filein.seek(0, 0);
    size = "";
    while True:
        b1 = filein.read(1).decode();
        if(b1 == "#"):
            break;
        size = size  + b1;
    size = int(size);
    i = 0;
    while True:
        if(i >= size):
            break;
        if(i + block >= size):
            size_temp = size -i;
        else:
             size_temp = block;
        sin = filein.read(block);
        if(size_temp == block):
            sout = encryptor.update(sin) + encryptor.finalize();
            fileout.write(sout)
        else:
            sout = encryptor.update(sin) + encryptor.finalize();
            _tmp_size = analyse(sout);
            if(_tmp_size != -1):
                sout = copy(sout, _tmp_size-1);
                fileout.write(sout);
        i = i + size_temp;
    return 0;

def file_encrypt(key, iv, fileinpath, fileoutpath):
    backend = default_backend();
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend);
    encryptor = cipher.encryptor();
    block = 31;
    filein = open(fileinpath, "rb");
    fileout = open(fileoutpath, "wb");
    filein.seek(0, 2);
    size = filein.tell();
    filein.seek(0, 0);
    fileout.write( ( str(size) + "#" ).encode());
    i = 0;
    while True:
        if(i >= size):
            break;
        if(i + block >= size):
            size_temp = size -i;
        else:
             size_temp = block;
        sin = data_array_Schreiben(filein.read(block));
        print(len(sin));
        if(size_temp == block):
            sout = encryptor.update(sin) + encryptor.finalize();
            fileout.write(sout)
        else:
            print(len(sin));
            sin = sin + "\0xFF".encode();
            print(len(sin));
            sout = encryptor.update(sin) + encryptor.finalize();
            fileout.write(sout)
        i = i + size_temp;
    return 0;

def copy(sin, size):
    out = b"";
    i = 0;
    while True:
        if(i >= len(sin)):
            break;
        if(i >= size):
            break;
        out = out + sin[i];
        i = i +1;
    return out;

def analyse(sout):
    out = sout.decode();
    i = len(out) -1;
    while True:
        if(i <= 0):
            break;
        if(out[i] == "\0xFF"):
            return i;
        i = i -1;
    return -1;


def array_remove(array, size):
    out_a = "";
    i = 0;
    while True:
        if(i >= len(array)):
            break;
        if(i >= size):
            break;
        if(size == len(out_a)):
            break;
        out_a = out_a + array[i];
        i = i +1;
    return out_a.encode();

def key_size_anpassen(key):
    if(len(key) > 32):
        key = array_remove(key, 32);
    while True:
        if(len(key) == 32):
            break;
        key = key + " ".encode();
    return key;

def data_array_Schreiben(indata):
    b1 = b" ";
    if(len(indata) < 32):
        indata = indata + b"\0xFF";
    while True:
        if(len(indata) >= 32):
            break;
        indata = indata + b1;
    return indata;

def cearte_a_test_file(spath):
    fileout1 = open(spath, "wb");
    endofline = "\0xFF";
    out = "";
    size = 31;
    for i in range(size):
        out = out + endofline;
    fileout1.write(out.encode());
    fileout1.close();
    return 0;



def main():
    key = "test11111111111111111111111111111111111111111111111111111214";
    key = key_size_anpassen(key);
    iv = os.urandom(16);
    cearte_a_test_file("1.txt");
    file_encrypt(key, iv, "1.txt", "out1.aes");
    file_decrypt(key, iv, "out1.aes", "2.txt");
    return 0;
main();
