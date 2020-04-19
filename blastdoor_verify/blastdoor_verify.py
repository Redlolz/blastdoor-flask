from base64 import b64encode, b64decode
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from riposte import Riposte
from riposte.printer import Palette
import os.path
import sys

peek = Riposte('[blastdoor]$ ')

@peek.command('help')
def help():
    peek.status("List of commands")
    peek.status("generate <filename>       - Generate a private RSA key")
    peek.status("publickey <filename>      - Generate public key from private key")
    peek.status("sign <filename> <message> - Sign message with private key")
    peek.status("exit                      - Exit the program")

@peek.command('generate')
def generate(filename: str):
    if not os.path.isfile(filename):
        # Generate RSA keypair
        peek.status("Generating RSA key...")
        key = RSA.generate(4096)
        enc_key = key.export_key()

        peek.status("Writing private key file...")
        public_key_file = open(filename, 'wb')
        public_key_file.write(enc_key)
        peek.success("Done")
    else:
        peek.error("File already exists!")

@peek.command('publickey')
def generate(filename: str):
    if os.path.isfile(filename):
        key = RSA.import_key(open(filename).read())
        peek.print(Palette.CYAN.format(key.publickey().export_key().decode('utf-8')))
    else:
        peek.error("File doesn't exist!")

@peek.command('sign')
def sign(filename: str, message: str):
    if os.path.isfile(filename):
        key = RSA.import_key(open(filename).read())
        h = SHA256.new(message.encode('utf-8'))
        signature = pkcs1_15.new(key).sign(h)
        peek.print(Palette.CYAN.format(b64encode(signature).decode('utf-8')))
    else:
        peek.error("File doesn't exists!")

@peek.command('exit')
def exit():
    peek.status("Goobye!")
    sys.exit()

peek.run()