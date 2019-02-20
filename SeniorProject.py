import time
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def EXIT():
    raise SystemExit


def getKey(Epassword):
    hasher = SHA256.new(Epassword.encode('utf-8'))
    return hasher.digest()


def Main():
    Epassword = input("Password: ")
    encrypt(getKey(Epassword), textfilename)
    print("Done.")
    os.remove("passwordfor" + applicationselect + ".txt")


def encrypt(key, filename):
    chunksize = 64*1024
    outputFile1 = "encrypted" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile1, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    global outputFile
    chunksize = 64*1024
    outputFile = filename[9:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def decryptionchoice():
    filename = input("File to decrypt: ")
    password = input("Password: ")
    decrypt(getKey(password), filename)
    input("Press Any Key to Continue and Re-Encrypt Your File")
    os.remove(outputFile)
    print("Done.")
    EXIT()


def EnterPasswords():
    global applicationselect
    global textfilename
    applicationselect = input("What do you want to enter a password for?:")
    txtfile = open("passwordfor" + applicationselect + ".txt", "w+")
    textfilename = ("passwordfor" + applicationselect + ".txt")

    txtfile.write("Username: \n")
    askuser = input("What is your username?:")
    txtfile.write(askuser)

    txtfile.write("\nPassword:\n")
    askpass = input("What is your password?:")
    txtfile.write(askpass)


def selection():
    while True:
        try:
            choice = int(input(
                "What do you want to do?: \n(1) Enter Passwords \n(2) Decrypt Passwords \n(3) \n(4)"
            ))
        except ValueError:
            ("Please enter a number!")
            continue
        if 0 < choice < 3:
            choices = {1: EnterPasswords,
                       2: decryptionchoice,
                       }
            choices[choice]()
            break
    else:
        print("That is not between 1 and 3! Try Again:")
        print("you entered: {} ".format(choice))
        time.sleep(1.5)
    Main()


selection()