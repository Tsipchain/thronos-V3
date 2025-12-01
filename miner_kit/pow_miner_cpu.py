#!/usr/bin/env python3
# Thronos CPU PoW Miner (generic kit)
#
# 1. Set your THR address in THR_ADDRESS.
# 2. Run:  pip install requests
# 3. Run:  python pow_miner_cpu.py

import hashlib
import time
import requests
import json
import sys

# Configuration
THR_ADDRESS = "THR_PUT_YOUR_ADDRESS_HERE"  # Replace with your actual THR address
SERVER_URL = "https://thrchain.up.railway.app" # Update if your server URL is different
DIFFICULTY = 5 # Default difficulty, should match server's expectation or be dynamic

def get_last_hash():
    """Fetches the last block hash from the Thronos server."""
    try:
        # Using the correct endpoint from server.py
        r = requests.get(f"{SERVER_URL}/last_block_hash", timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("last_hash", "0" * 64)
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error fetching last hash: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error fetching last hash: {e}")
        return None

def mine_block(last_hash):
    """
    Simple CPU mining:
    - Takes last_hash
    - Tries nonces until SHA256(last_hash + thr_address + nonce) has
      DIFFICULTY leading '0's
    - Returns the block payload ready for submission
    """
    target_prefix = "0" * DIFFICULTY
    
    print(f"⛏️  Starting mining for {THR_ADDRESS} (difficulty={DIFFICULTY})")
    print(f"   Last block hash: {last_hash}")

    nonce = 0
    start = time.time()
    
    # Update status every 5 seconds
    last_status_time = start
    
    while True:
        # Check if we should stop/restart (e.g. if too much time passed, maybe new block found)
        if time.time() - start > 60:
             # Every 60 seconds, check if the last hash changed on server to avoid mining on stale blocks
             current_server_hash = get_last_hash()
             if current_server_hash and current_server_hash != last_hash:
                 print("🔄 New block found on network. Restarting mining...")
                 return None
             # Reset start time to continue checking periodically
             start = time.time() 

        nonce_str = str(nonce).encode()
        # The data format must match what the server expects for verification
        # Based on server logic (assumed standard PoW): hash(prev_hash + sender + nonce)
        data = (last_hash + THR_ADDRESS).encode() + nonce_str
        h = hashlib.sha256(data).hexdigest()

        if time.time() - last_status_time > 5:
            elapsed = time.time() - start
            hashrate = nonce / elapsed if elapsed > 0 else 0
            print(f"[{THR_ADDRESS}] nonce={nonce} hash={h[:16]}... ({hashrate:.1f} H/s)")
            last_status_time = time.time()

        if h.startswith(target_prefix):
            duration = time.time() - start
            print(f"✅ Found valid nonce after {nonce} tries in {duration:.1f}s")
            print(f"   Hash: {h}")
            block = {
                "thr_address": THR_ADDRESS,
                "nonce": nonce,
                "pow_hash": h,
                "prev_hash": last_hash,
                # Add timestamp if server requires it, usually server sets it
            }
            return block

        nonce += 1
        # Add a tiny sleep to prevent 100% CPU usage if needed, or remove for max speed
        # time.sleep(0.0001) 

def submit_block(block):
    """Submits the mined block to the server."""
    try:
        # Endpoint assumed to be /submit_block or similar. 
        r = requests.post(f"{SERVER_URL}/submit_block", json=block, timeout=10)
        if r.status_code == 200:
            print(f"📬 Submission successful: {r.json()}")
            return True
        else:
            print(f"⚠️ Submission failed: {r.status_code} - {r.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error submitting block: {e}")
        return False
    except Exception as e:
        print(f"❌ Error submitting block: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        THR_ADDRESS = sys.argv[1]
    
    if "THR_PUT_YOUR_ADDRESS_HERE" in THR_ADDRESS:
        print("⚠️  Please set your THR_ADDRESS in the script or pass it as an argument.")
        print("   Usage: python pow_miner_cpu.py <YOUR_THR_ADDRESS>")
        sys.exit(1)

    print(f"🚀 Thronos CPU Miner started for address: {THR_ADDRESS}")
    print(f"📡 Server: {SERVER_URL}")
    
    while True:
        last_hash = get_last_hash()
        if last_hash:
            mined_block = mine_block(last_hash)
            if mined_block:
                submit_block(mined_block)
            
            # Small delay before next attempt
            time.sleep(2)
        else:
            print("⏳ Waiting for server connection...")
            time.sleep(5)