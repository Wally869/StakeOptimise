import type { NetworkSettings } from "$lib/network-utils";

export const COSMOS_MAINNET: NetworkSettings = {
    chain_id: "cosmoshub-4",
    rpc: "https://rpc-cosmoshub.blockapsis.com",
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