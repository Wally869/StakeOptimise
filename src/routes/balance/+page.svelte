<script lang="ts">
	import { COSMOS_TESTNET } from "$lib/settings/cosmos_testnet";
	import { StargateClient } from "@cosmjs/stargate";

    const network_settings = COSMOS_TESTNET;
    
	async function get_balance() {
        await window.keplr.enable(network_settings.chain_id);
        const offlineSigner = window.keplr.getOfflineSigner(network_settings.chain_id);
               

        // You can get the address/public keys by `getAccounts` method.
        // It can return the array of address/public key.
        // But, currently, Keplr extension manages only one address/public key pair.
        // XXX: This line is needed to set the sender address for SigningCosmosClient.
        const accounts = await offlineSigner.getAccounts();

        let client = await StargateClient.connect(network_settings.rpc);

        let balance = await client.getBalance(accounts[0].address, "uatom");
        console.log(`balance: ${JSON.stringify(balance)}`)

        
        console.log(`owns: ${parseFloat(balance.amount) / Math.pow(10, network_settings.token.decimals)}`)
    }
</script>

<button on:click={() => get_balance()}>Get Balance</button>
