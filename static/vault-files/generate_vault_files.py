# generate_vault_files.py
import os
import base64

vault_dir = "static/vault-files"
os.makedirs(vault_dir, exist_ok=True)

files = {
    "deepnote.txt": "FLAG-VAULT-ALPHA123",
    "cipherdump.txt": "FLAG-VAULT-BETA456",
    "encodings.txt": "FLAG-VAULT-GAMMA789",
    "matrixcode.txt": "FLAG-VAULT-DELTA000"
}

for filename, flag in files.items():
    content = base64.b64encode(flag.encode()).decode()  # Simulate "encryption"
    with open(os.path.join(vault_dir, filename), "w") as f:
        f.write(f":: Encrypted Content ::\n{content}\n")
print("✅ Vault files created.")

