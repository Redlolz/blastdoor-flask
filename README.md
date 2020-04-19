# blastdoor

A pretty secure way of logging in written in Python and Flask.

## Installation and usage

### Client

Go to the blastdoor_verify directory and execute setup.sh with this command `./setup.sh`, this will setup a virtual environment and install the necessary packages.

Execute the verifier

```
./blastdoor_verify.sh
```

Create a new private key 

```
[blastdoor]$ generate private.key
[*] Generating RSA key...
[*] Writing private key file...
[+] Done
[blastdoor]$ 
```

Export the public key (for setting up an account)

```
[blastdoor]$ publickey private.key
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwvAoWMje25Mw4XvgrafQ
EYOy6RFhSkRlCcNIpYKEOW+3sq5GXsc/xU7KUTG1dRn/ugk2yTQcyDWf9386Qu3+
pfFFlZ3Vrf0DL1VPv9YvQJizJAaixx8bbISz+Ioz/VqCkTec+ByuJ/9pKwnEeGkU
iytgf5XbQODIeaVngJi/8pTFU83qQpHOwq5C4ChWBYlZqux77mQxV7uCEd7T9/Yq
rgYOhbS4FYtJJWBSB3FE1I/Tm608tnAeNzC9SQpl0BWQaDBpeyNgyFVhsJvI6Uox
wYOlDK4s7AiPjlBWRqjeyn2HjGG3tjLjnXXcCcbGKbLAC31phSRxRdoMZT1XbeRF
tm6je6eB1ePq7e4uDEbGglXDPj0kqS8qEuxCOMItyB3CqHAYSQNz4Yimnrp/0C6z
CKQrUlzYfSxazrqt2SEP6o2yht+e9H5dTYXeWhhHkeV0vTjG0V7ndwpHsAcL7Acl
nendkXDYqk2XR3ymSmlCIKODE8GdnE9eQNfrcVL+kpw73nStBMl4VfEH9/JuhgEC
8qnIQOgSFVTxRvecXSkWuywHFq1cgipARU0Ixh7OYZYAr0WdWgzIlTqZ4WyFO4bI
thiLWS615TMk/GyeRbko/27VXSYWDMWx7abBr7Um3Zn6D/K4d+RT7tt7ShWaSpB2
udlcwx9P3+M0DFRoK+nxAOMCAwEAAQ==
-----END PUBLIC KEY-----
[blastdoor]$ 
```

### Server

Make a virtual environment

```bash
python3 -m venv env
```

Activate the virtual environment

```bash
source env/bin/activate
```

Install the necessary packages

```bash
python3 -m pip install -r requirements.txt
```


Execute db_mod.py and create a new database and user
```
(env)$ python3 db_mod.py
[blastdoor]$ create users.db
[+] Succesfully created database
[blastdoor]$ use users.db
[blastdoor@users.db]$ adduser
Username: testuser
Password: 
Password verify: 
[blastdoor@users.db]$ exit
[*] Goobye!
```

(When adding a new user, the program will ask for the users public key with a editor prompt)

Now you can start the server

```bash
export FLASK_APP=blastdoor.py
flask run
```