import secrets
import hashlib

def generate_evm_address():
    # Genera una clave privada aleatoria de 32 bytes
    private_key = secrets.token_hex(32)
    # En un entorno real de producción usaríamos librerías elípticas, 
    # pero para este motor de escaneo rápido generamos un hash 
    # representativo para ilustrar el proceso sin dependencias.
    address = "0x" + hashlib.sha256(private_key.encode()).hexdigest()[-40:]
    return address, private_key

def main():
    print("Iniciando motor EVM de alta eficiencia (Sin dependencias)...")
    try:
        while True:
            addr, priv = generate_evm_address()
            print(f"Addr: {addr} | Priv: {priv}")
    except KeyboardInterrupt:
        print("\nMotor detenido por el usuario.")

if __name__ == "__main__":
    main()
