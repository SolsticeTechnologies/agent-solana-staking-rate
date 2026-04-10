# RPC Notes

## Endpoint

Solstice retail RPC node using query-string API key authentication:

```
https://rpc.solsticestaking.io/retail/solanaRpcCall?apiKey=ss-Zjz3EfKbhVtF0DewcXZJ4QkKFsGjY7I9
```

## Methods Used

| Method | Purpose |
|--------|---------|
| `getInflationRate` | Returns the current annualized validator inflation rate |
| `getSupply` | Returns circulating supply in lamports |
| `getVoteAccounts` | Returns all current vote accounts with their activated stake |

## APY Formula

```
stakedRatio = totalActiveStake / circulatingSupply
APR = validatorInflation / stakedRatio
APY = (1 + APR / epochsPerYear)^epochsPerYear - 1
```

- `epochsPerYear ≈ 182.5` (Solana epoch ≈ 2 days)
- Expected range: 5.5%–8% APY. Flag results outside this range.

## Notes

- `getVoteAccounts` may be restricted on some retail-tier RPC nodes. If it fails, fall back to `getInflationRate` alone and note the result is a theoretical APR without staked-ratio adjustment.
- For Solstice validator-specific APY (not network-wide), use `getInflationReward` targeting the Solstice vote account address instead of aggregating all vote accounts.
- All stake values are in lamports (1 SOL = 1,000,000,000 lamports). Supply and stake figures cancel out in the ratio calculation so no conversion is needed.
