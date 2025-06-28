from dataclasses import dataclass
from typing import Optional, Dict
from enum import Enum
from typing import List

@dataclass
class Keyring:
    owner: str
    name: str
    default: bool
    def __str__(self):
        default_status = "DEFAULT" if self.default else "NODEFAULT"
        return f"  Label={self.name} - Owner={self.owner} - {default_status}"

@dataclass
class Certificate:
    #Information from RACF
    owner: str
    label: str
    privatekey: bool
    keyringInfo: List[Keyring]
    subject: Dict
    # Additional information to renew (optional)
    newlabel: Optional[str] = None
    explabel: Optional[str] = None
    bkoutlabel: Optional[str] = None

    def __str__(self):
        keyrings_str = '\n'.join(str(kr) for kr in self.keyringInfo) if self.keyringInfo else "NO KEYRING"
        subject_str = '\n    '.join(f"{k}: {v}" for k, v in self.subject.items())
        optional_fields = []
        if self.newlabel:
            optional_fields.append(f"New Label: {self.newlabel}")
        if self.explabel:
            optional_fields.append(f"Expiring Label: {self.explabel}")
        if self.bkoutlabel:
            optional_fields.append(f"Backup Label: {self.bkoutlabel}")
        optional_str = '\n'.join(optional_fields)
        return (
f"""Label: {self.label}
Owner: {self.owner}
Private Key: {self.privatekey}
Keyring Information:
{keyrings_str}
Subject's Name:
    {subject_str}
"""+ (f"{optional_str}\n" if optional_str else ""))
    def certCompare(self, other: 'Certificate') -> bool:
        return self.subject == other.subject and self.label == other.label