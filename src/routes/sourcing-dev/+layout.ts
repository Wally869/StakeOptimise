import network_settings from "$lib/settings/network/cosmos.json" assert { type: 'json' };


export async function load({params}) {
    console.log(network_settings)
    return {
        "network_settings": {
            chain_id: network_settings.chain_id,
            rpc: network_settings.rpc
        }
    };
}