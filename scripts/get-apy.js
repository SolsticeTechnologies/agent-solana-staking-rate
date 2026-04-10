#!/usr/bin/env node

const RPC = "https://rpc.solsticestaking.io/retail/solanaRpcCall?apiKey=ss-Zjz3EfKbhVtF0DewcXZJ4QkKFsGjY7I9";

async function rpc(method, params = []) {
  const res = await fetch(RPC, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
  });
  const json = await res.json();
  if (json.error) throw new Error(`RPC error [${method}]: ${json.error.message}`);
  return json.result;
}

async function main() {
  // 1. Current inflation rate
  const inflation = await rpc("getInflationRate");
  const validatorInflation = inflation.validator; // annualized

  // 2. Total supply
  const supply = await rpc("getSupply", [{ excludeNonCirculatingAccountsList: true }]);
  const circulating = supply.value.circulating; // in lamports

  // 3. Active stake from vote accounts
  const votes = await rpc("getVoteAccounts");
  const activeStake = votes.current.reduce((sum, v) => sum + v.activatedStake, 0);

  // 4. Staked ratio
  const stakedRatio = activeStake / circulating;

  // 5. APR = inflation going to stakers / fraction that is staked
  const apr = validatorInflation / stakedRatio;

  // 6. Epochs per year ≈ 182.5 (epoch ~2 days)
  const epochsPerYear = 365 / 2;
  const apy = (Math.pow(1 + apr / epochsPerYear, epochsPerYear) - 1);

  console.log(JSON.stringify({
    apr: (apr * 100).toFixed(4),
    apy: (apy * 100).toFixed(4),
    stakedRatio: (stakedRatio * 100).toFixed(2),
    epoch: inflation.epoch,
    validatorInflationRaw: validatorInflation,
  }, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
