//import network_settings from "$lib/settings/network/cosmos.json" assert { type: 'json' };

import { COSMOS_TESTNET as network_settings } from '$lib/settings/cosmos_testnet.js';


export const ssr = false;
export const csr = true;
export const prerender = false;

export async function load({params}) {
    return {
        "network_settings": {
            token: network_settings.token,
            chain_id: network_settings.chain_id,
            rpc: network_settings.rpc,
            fees: network_settings.fees
        }
    };
}