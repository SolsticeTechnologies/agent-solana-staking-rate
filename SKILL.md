---
name: solana-staking-rate
description: Fetches the current Solana network staking APY using live RPC data from Solstice's node.
version: 1.0.0
requirements:
  - node
metadata:
  openclaw:
    emoji: "◎"
---

## Instructions

When the user asks about the current Solana staking rate, staking APY, staking yield, or SOL rewards:

1. Run `scripts/get-apy.js` using the Bash tool.
2. Parse the JSON output and present the APY as a percentage rounded to two decimal places.
3. Include the epoch number and the staked ratio for context.
4. If the script fails, report the error and suggest checking the RPC endpoint.

## Rules
- Always source data from the live RPC call, never use hardcoded values.
- If the result deviates more than 1.5% from the expected 5.5–8% range, flag it as suspicious.
- Present results in both APR (raw inflation) and APY (with epoch compounding) if asked.
