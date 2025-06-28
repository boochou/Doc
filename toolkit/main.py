from app.models.models import Certificate, Keyring
from app.services.commandGenerator import CmdGenCert
from app.services.utilies import *

keyring = Keyring(owner="admin", name="MAIN", default=True)
keyring1 = Keyring(owner="xxxxxxxx", name="---------", default=False)
cert = Certificate(label="CertA", privatekey=True, keyringInfo=[keyring,keyring1], 
                   subject={"CN": "example.com", 
                            "O": "MIS team",
                            "L": "Mycomp",
                            "OU": "AUS",
                            "SP": "Melbourne",
                            "C": "LA"}, owner='CHAU', newlabel='CERT_25',bkoutlabel="CERT_X25",explabel='CERT_23')
print(cert)
cmd_gen = CmdGenCert(cert, system="zOS", desfile="cert.jcl", log=False)
cmd_gen.cmdGenImpl()
cmd_gen.cmdGenBkt()


