# app/utils/utilities.py

from pathlib import Path
from typing import Dict
import importlib
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from OpenSSL import crypto
import base64
from pathlib import Path

class Utilities:

    @staticmethod
    def render_template(template_name: str, values: Dict[str, str]) -> str:
        # Import template module dynamically
        template_module = importlib.import_module("app.value.CertTemplate")
        try:
            raw_template = getattr(template_module, template_name)
        except AttributeError:
            raise ValueError(f"Template {template_name} not found in CertTemplate.py")

        try:
            rendered = raw_template.format(**values)
        except KeyError as e:
            raise ValueError(f"Missing value for template variable: {e}")
        return rendered
    @staticmethod
    def saveToFile(output_dir: Path,template_name: str,data):
         # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write to file
        output_file = output_dir / f"{template_name}.txt"
        output_file.write_text(data, encoding="utf-8")

        print(f"[LOG] Rendered {template_name} to {output_file}")
    
    @staticmethod
    def convert_certificate_to_base64(path: Path, output_txt: Path):
        ext = path.suffix.lower()
        certs = []

        if ext == ".pem":
            with open(path, "rb") as f:
                data = f.read()
            certs = [x509.load_pem_x509_certificate(data, default_backend())]

        elif ext == ".der":
            with open(path, "rb") as f:
                data = f.read()
            certs = [x509.load_der_x509_certificate(data, default_backend())]

        elif ext == ".p7b":
            with open(path, "rb") as f:
                data = f.read()
            pkcs7 = crypto.load_pkcs7_data(crypto.FILETYPE_ASN1, data)
            certs = pkcs7.get_certificates() or []

        else:
            raise ValueError("Unsupported format: only .pem, .der, .p7b")

        # Lọc ra non-root certificates (không có Authority Key ID = Subject Key ID)
        filtered = []
        for cert in certs:
            if hasattr(cert, "extensions"):
                try:
                    aki = cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier)
                    ski = cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier)
                    if aki.value.key_identifier != ski.value.digest:
                        filtered.append(cert)
                except Exception:
                    filtered.append(cert)  # nếu không có AKI thì giữ lại
            else:
                filtered.append(cert)

        with open(output_txt, "w") as f_out:
            for cert in filtered:
                der = cert.public_bytes(crypto.FILETYPE_ASN1) if isinstance(cert, crypto.X509) \
                    else cert.public_bytes(default_backend())
                b64 = base64.b64encode(der).decode()
                f_out.write(b64 + "\n")

        print(f"Converted and saved to {output_txt}")
