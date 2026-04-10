---
name: solana-staking-rate
description: Fetches the current Solana network staking APY using live RPC data from Solstice's node.
version: 1.1.0
requirements:
  - python3
metadata:
  openclaw:
    emoji: "◎"
---

## Instructions

When the user asks about the current Solana staking rate, staking APY, staking yield, or SOL rewards:

1. Run `scripts/get-apy.py` using the Bash tool: `python3 scripts/get-apy.py`
2. Parse the JSON output and present results clearly:
   - **APY** (epoch-compounded) — primary number to highlight
   - **APR** (raw inflation-based)
   - **Staked Ratio** — % of circulating supply actively staked
   - **Epoch** — current network epoch for reference
   - **Active Stake** and **Circulating Supply** in SOL
3. If `get-apy.py` fails, fall back to `scripts/get-apy.js` with: `node scripts/get-apy.js`
4. If both fail, report the error and suggest checking the RPC endpoint.

## Rules
- Always run the script for live data — never estimate or use hardcoded values.
- Report exact values from the script output, rounded to 2 decimal places for display.
- If APY result is outside 5.5–8% range, flag it as suspicious and include the raw numbers.
- Present APR and APY as distinct values — APY is always slightly higher due to epoch compounding.
