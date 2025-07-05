import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ETHERSCAN_API_KEY")
TOKEN_ADDRESS = os.getenv("TOKEN_CONTRACT_ADDRESS").lower()

ETHERSCAN_URL = "https://api.etherscan.io/api"

def get_token_holders():
    print(f"🔍 Scanning token holders for {TOKEN_ADDRESS}...")
    holders = {}
    page = 1
    offset = 100
    while True:
        url = f"{ETHERSCAN_URL}?module=token&action=tokenholderlist&contractaddress={TOKEN_ADDRESS}&page={page}&offset={offset}&apikey={API_KEY}"
        response = requests.get(url).json()
        if 'result' not in response or not response['result']:
            break
        for entry in response['result']:
            addr = entry['HolderAddress'].lower()
            balance = int(entry['TokenHolderQuantity'])
            holders[addr] = holders.get(addr, 0) + balance
        print(f"Page {page} parsed...")
        page += 1
    return holders

def analyze_distribution(holders):
    total = sum(holders.values())
    sorted_holders = sorted(holders.items(), key=lambda x: x[1], reverse=True)
    print(f"👥 Total holders: {len(sorted_holders)}")
    print(f"💰 Total tokens: {total / 1e18:.4f}")
    print("🏆 Top 5 holders:")
    for i, (addr, bal) in enumerate(sorted_holders[:5]):
        pct = (bal / total) * 100
        print(f"{i+1}. {addr} - {bal / 1e18:.4f} tokens ({pct:.2f}%)")
    top10_total = sum(bal for _, bal in sorted_holders[:10])
    print(f"🔗 Top 10 holders own: {(top10_total / total) * 100:.2f}%")

def main():
    holders = get_token_holders()
    if holders:
        analyze_distribution(holders)
    else:
        print("No holders data found or API limit reached.")

if __name__ == "__main__":
    main()
