<script lang="ts">
	import { create_client, get_validator_data, type NetworkSettings, type StakingClient } from '$lib/network-utils';
    import type { Keplr } from '@keplr-wallet/types';
	import type { Validator } from '$lib/types/pytypes';
	import { onMount } from 'svelte';

	let validators_data: Validator[] = [];

    export let data;

	const RPC = 'https://rpc-cosmoshub.blockapsis.com';

	let query_client: StakingClient;
	onMount(async () => {
        // query network info and validators data 
        
        

        console.log(`loaded settings: ${data.network_settings.chain_id}`);
		query_client = await create_client(data.network_settings.rpc);
		validators_data = await get_validator_data(query_client);
		console.log(`there are ${validators_data.length} bounded validators`);
	});

	// try to connect
	async function connect_four(): Promise<Keplr | null> {
		const chainId = 'cosmoshub-4';

		if (window.keplr) {
			// Enabling before using the Keplr is recommended.
			// This method will ask the user whether to allow access if they haven't visited this website.
			// Also, it will request that the user unlock the wallet if the wallet is locked.
			await window.keplr.enable(chainId);

			const offlineSigner = window.keplr.getOfflineSigner(chainId);

			// You can get the address/public keys by `getAccounts` method.
			// It can return the array of address/public key.
			// But, currently, Keplr extension manages only one address/public key pair.
			// XXX: This line is needed to set the sender address for SigningCosmosClient.
			const accounts = await offlineSigner.getAccounts();
            console.log(accounts);

			// Initialize the gaia api with the offline signer that is injected by Keplr extension.
            /*
			const cosmJS = new SigningCosmosClient(
				'https://lcd-cosmoshub.keplr.app',
				accounts[0].address,
				offlineSigner
			);
            */

            return window.keplr;
		} else {
            return null;
        }
	}
</script>

<div class="w-full">
	<div class="mx-auto">
        {data.network_settings.chain_id}

		<button class="border border-2" on:click={() => connect_four()}>Connect</button>

		<table>
			<tr>
				<th>Moniker</th>
				<th>Address</th>
				<th>Staked</th>
				<th>Commission Rate</th>
			</tr>
			{#each validators_data as validator_data}
				<tr>
					<td>{validator_data.moniker}</td>
					<td>{validator_data.address}</td>
					<td class="text-right">{validator_data.curr_stake}</td>
					<td>{validator_data.commission_rate}</td>
				</tr>
			{/each}
		</table>
	</div>
</div>
