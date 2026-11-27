import os
import time
import sqlite3
from eth_account import Account
from web3 import Web3

# Habilitar generación de cuentas no deterministas
Account.enable_unaudited_hdwallet_features()

# Configuración del Nodo RPC (BSC - Binance Smart Chain)
RPC_URL = "https://bsc-dataseed.binance.org/"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Configuración de Persistencia
DB_FILE = "found_wallets_evm.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS findings 
                  (address TEXT, private_key TEXT, balance REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def scan_batch(batch_size=100):
    for _ in range(batch_size):
        acct = Account.create()
        address = acct.address
        private_key = acct.key.hex()
        
        # Consulta de saldo nativo (BNB)
        try:
            balance = w3.eth.get_balance(address)
            balance_bnb = w3.from_wei(balance, 'ether')
            
            if balance > 0:
                print(f"\n!!! HALLAZGO ENCONTRADO !!!")
                print(f"Dirección: {address}")
                print(f"Saldo: {balance_bnb} BNB")
                cursor.execute("INSERT INTO findings (address, private_key, balance) VALUES (?, ?, ?)", 
                               (address, private_key, float(balance_bnb)))
                conn.commit()
        except Exception as e:
            continue
    return batch_size

print("Iniciando motor EVM (BSC) de alta eficiencia...")
while True:
    try:
        scanned = scan_batch(50)
        print(f"Lote escaneado: {scanned} carteras. Seguimos...")
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
