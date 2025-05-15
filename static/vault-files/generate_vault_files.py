import os
import base64

vault_dir = "static/vault-files"
os.makedirs(vault_dir, exist_ok=True)

files = {
    "vault_alpha.zip": "FLAG-VAULT-ALPHA123",
    "coredata.gpg": "FLAG-VAULT-BETA456",
    "stego_image.png": "FLAG-VAULT-GAMMA789",
    "locked.docx": "FLAG-VAULT-DELTA000",
    "archive_payload.tar.gz": "FLAG-VAULT-OMEGA321",
    "vault_hint.txt": "Try strings, steg tools or brute-force."
}

for filename, flag in files.items():
    content = base64.b64encode(flag.encode()).decode()  # Simulate "encryption"
    with open(os.path.join(vault_dir, filename), "w") as f:
        f.write(f":: Encrypted Content ::\n{content}\n")
print("✅ Vault files created.")
