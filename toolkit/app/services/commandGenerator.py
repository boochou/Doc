# app/services/command_generator.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from app.models.models import Certificate
from app.services.utilies import *
from ..value.CertTemplate import *
# from app.models.acl import ACL 

class CommandGenerator(ABC):
    def __init__(self, log: bool = False, data: Optional[object] = None, system: str = "", desfile: str = ""):
        self.log = log
        self.data = data
        self.system = system
        self.desfile = desfile

    @abstractmethod
    def cmdGenImpl(self) -> None:
        pass

    @abstractmethod
    def cmdGenBkt(self) -> None:
        pass

    def genJobCard(self,jc="IMPLMNT",member=None,typ = 'IMPL'):
        template_name = "JC_LOG" if self.log else "JC_NOLOG"
        value ={
            "jc": jc,
            "class": self.system,
            "desfile": self.desfile,
            "type": typ,
            "member": member
        }
        return Utilities.render_template(template_name,value)
    def _save_commands(self, cmd_all: set, prefix: str, job_type: str):
        output_dir = Path(__file__).parent.parent / "temp"
        pre = "#" if prefix == "IMPL" else "$"
        for cmd, descr, idx in cmd_all:
            if self.log:
                jc = self.genJobCard(descr, f"#{prefix}0{idx}", job_type)
                Utilities.saveToFile(output_dir, f"${prefix}0{idx}", jc)
                Utilities.saveToFile(output_dir, f"#{prefix}0{idx}", cmd)
            else:
                full_cmd = self.genJobCard(descr) + cmd
                Utilities.saveToFile(output_dir, f"{pre}{idx}{descr}", full_cmd)   

class CmdGenCert(CommandGenerator):
    def __init__(self, certificate: Certificate, **kwargs):
        super().__init__(data=certificate, **kwargs)
        self.data: Certificate = certificate
        if self.data.owner != 'SITE' and  self.data.owner != 'CERTAUTH':
            self.data.owner = f"ID({self.data.owner})"
        self.values = self._init_template_values()

    def _init_template_values(self) -> dict:
        subject_str = "SUBJECTSDN(" + " +\n    ".join(
            f"{k}('{v}')" for k, v in self.data.subject.items()
        ) + ")"
        return {
            "Owner": self.data.owner,
            "New Label": self.data.newlabel,
            "Subject_Name": subject_str,
            "CSR": self.desfile + ".CSR",
            "CER": self.desfile + ".CER",
            "Current Label": self.data.label,
            "Expiring Label": self.data.explabel
        }
    def cmdGenKeyring(self):
        template = ["_5ADDKR1","_6RMVKR1"]
        add_cmd = ""
        remove_cmd = ""
        for keyring in self.data.keyringInfo:
            self.values["Keyring Owner"] = keyring.owner
            self.values["Keyring"] = keyring.name
            self.values["Key Mode"] = "DEFAULT" if keyring.default else ""
            add_cmd += Utilities.render_template(template[0], self.values)
            remove_cmd += Utilities.render_template(template[1], self.values)
        add_cmd += REFRESH_KEYRING
        remove_cmd += REFRESH_KEYRING
        return {
            (add_cmd,template[0][2:],template[0][1]),(remove_cmd,template[1][2:],template[1][1])
        }
 
    def cmdGenImpl(self) -> None:
        print(f"Generating implementation command for certificate: {self.data.label}")     
        impl_templates = {"_3REOLD", "_4ADDCER"}
        if self.data.privatekey:
            impl_templates.update({"_1CRTCER", "_2CRTCSR"})
            
        cmd_all = {
        (Utilities.render_template(tmpl, self.values), tmpl[2:], tmpl[1])
        for tmpl in impl_templates
        }
            
        if self.data.keyringInfo:
            keyring_cmds = self.cmdGenKeyring()
            cmd_all.update(keyring_cmds)
               
        output_dir = Path(__file__).parent.parent / "temp"
        super()._save_commands(cmd_all, prefix="IMPL", job_type="IMPL") 
            
    def cmdGenBkt(self) -> None:
        print(f"Generating backup command for certificate: {self.data.label}")
        #UPDATE VALUE TO GEN BKT
        self.values["Expiring Label"] = self.data.bkoutlabel
        self.values["New Label"] = self.data.explabel

        cmd_all = {
        (Utilities.render_template(tmpl, self.values), tmpl[2:], tmpl[1])
        for tmpl in {"_3REOLD","_4CHGCER"}
        }
            
        if self.data.keyringInfo:
            keyring_cmds = self.cmdGenKeyring()
            cmd_all.update(keyring_cmds)
               
        output_dir = Path(__file__).parent.parent / "temp"
        super()._save_commands(cmd_all, prefix="BKOUT", job_type="BKT") 

# class CmdGenGrantAccess(CommandGenerator):
#     def __init__(self, acl: ACL, **kwargs):
#         super().__init__(data=acl, **kwargs)
#         self.data: ACL = acl

#     def cmdGenImpl(self) -> None:
#         print(f"Generating implementation command for ACL access")
#         # Placeholder
#         print(f"GRANT ACCESS {self.data}")

#     def cmdGenBkt(self) -> None:
#         print(f"Generating backup command for ACL access")
#         # Placeholder
#         print(f"BACKUP ACCESS {self.data}")
