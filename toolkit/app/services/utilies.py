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
    
