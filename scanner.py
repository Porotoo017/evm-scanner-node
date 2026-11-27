import secrets
import hashlib
import time

OUTPUT_FILE = "found_wallets.txt"

def generate_evm_address():
    # Genera una clave privada aleatoria de 32 bytes
    private_key = secrets.token_hex(32)
    # Dirección derivada para simulación criptográfica pura sin librerías externas
    address = "0x" + hashlib.sha256(private_key.encode()).hexdigest()[-40:]
    return address, private_key

def main():
    print(f"Iniciando motor EVM con guardado automático en '{OUTPUT_FILE}'...")
    count = 0
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        try:
            while True:
                addr, priv = generate_evm_address()
                f.write(f"Addr: {addr} | Priv: {priv}\n")
                count += 1
                if count % 10 == 0:
                    f.flush()
                    print(f"[{count} carteras guardadas] Última: {addr}")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print(f"\nMotor detenido. Total registrado: {count} carteras en {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
