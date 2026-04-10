#!/usr/bin/env python3

import json
import urllib.request
import urllib.error
import sys

RPC = "https://rpc.solsticestaking.io/retail/solanaRpcCall?apiKey=ss-Zjz3EfKbhVtF0DewcXZJ4QkKFsGjY7I9"

def rpc(method, params=None):
    if params is None:
        params = []
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }).encode("utf-8")
    req = urllib.request.Request(
        RPC,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if "error" in result:
        raise RuntimeError(f"RPC error [{method}]: {result['error']['message']}")
    return result["result"]

def main():
    # 1. Current inflation rate
    inflation = rpc("getInflationRate")
    validator_inflation = inflation["validator"]  # annualized

    # 2. Total circulating supply (in lamports)
    supply = rpc("getSupply", [{"excludeNonCirculatingAccountsList": True}])
    circulating = supply["value"]["circulating"]

    # 3. Active stake from all current vote accounts
    votes = rpc("getVoteAccounts")
    active_stake = sum(v["activatedStake"] for v in votes["current"])

    # 4. Staked ratio
    staked_ratio = active_stake / circulating

    # 5. APR = validator inflation / staked ratio
    apr = validator_inflation / staked_ratio

    # 6. APY with epoch compounding (~182.5 epochs/year, epoch ≈ 2 days)
    epochs_per_year = 365 / 2
    apy = (1 + apr / epochs_per_year) ** epochs_per_year - 1

    print(json.dumps({
        "apr":                  f"{apr * 100:.4f}",
        "apy":                  f"{apy * 100:.4f}",
        "stakedRatio":          f"{staked_ratio * 100:.2f}",
        "epoch":                inflation["epoch"],
        "validatorInflationRaw": validator_inflation,
        "activeStakeSOL":       round(active_stake / 1e9, 2),
        "circulatingSOL":       round(circulating / 1e9, 2),
    }, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
