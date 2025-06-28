import subprocess

def convert_p7b_to_pem_base64(p7b_path: str, output_pem_path: str):
    cmd = [
        "openssl", "pkcs7",
        "-inform", "DER",              # or "PEM" depending on your file format
        "-in", p7b_path,
        "-print_certs",
        "-out", output_pem_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Converted to PEM and saved to: {output_pem_path}")

# Example usage:
convert_p7b_to_pem_base64("cert.p7b", "cert.pem")
