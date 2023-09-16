import type { NetworkSettings } from "$lib/network-utils";

export const COSMOS_TESTNET: NetworkSettings = {
    chain_id: "theta-testnet-001",
    rpc: "https://rpc.sentry-01.theta-testnet.polypore.xyz",
    token: {
        base: "atom",
        denom: "uatom",
        decimals: 6
    },
    fees: {
        "denom": "uatom",
        "fixed_min_gas_price": 0.0025
    }
}