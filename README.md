# ◎ Solana Staking Rate — OpenClaw Skill

An [IronClaw](https://agent.near.ai) skill that fetches live Solana network staking APY directly from Solstice's RPC node.

## What it does

Responds to natural language queries like:
- *"What's the current Solana staking APY?"*
- *"What's the staking rate for SOL?"*
- *"Tell me about Solana network yields"*

Returns exact, live values — no estimates, no hardcoded numbers.

## How it works

Three sequential RPC calls to `rpc.solsticestaking.io`:

| Call | Purpose |
|------|---------|
| `getInflationRate` | Annualized validator inflation rate |
| `getSupply` | Circulating supply in lamports |
| `getVoteAccounts` | Active stake across all current validators |

**Formula:**
```
stakedRatio = totalActiveStake / circulatingSupply
APR         = validatorInflation / stakedRatio
APY         = (1 + APR / epochsPerYear)^epochsPerYear − 1
```
Epochs per year ≈ 182.5 (Solana epoch ≈ 2 days).

## Sample output

```json
{
  "apr": "5.6200",
  "apy": "5.7820",
  "stakedRatio": "69.74",
  "epoch": 954,
  "validatorInflationRaw": 0.03921,
  "activeStakeSOL": 400341823.45,
  "circulatingSOL": 574198234.12
}
```

## Installation

```bash
git clone https://github.com/SolsticeTechnologies/agent-staking-rate-solana \
  ~/.openclaw/skills/agent-staking-rate-solana
```

## Structure

```
├── SKILL.md                  # OpenClaw skill config + agent instructions
├── openclaw.json             # Registers and enables the skill
├── scripts/
│   ├── get-apy.py            # Primary script (Python 3, no dependencies)
│   └── get-apy.js            # Fallback script (Node.js)
└── references/
    └── rpc-notes.md          # RPC docs and formula reference
```

## Requirements

- Python 3 (primary) or Node.js (fallback)
- Network access to `rpc.solsticestaking.io`

---

Built for [Solstice Technologies](https://solsticestaking.io) · Powered by [IronClaw](https://agent.near.ai)
