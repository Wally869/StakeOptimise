<script lang="ts">
	import { onMount } from 'svelte';

	import Separator from '$lib/components/ui/separator/separator.svelte';
	import StakeParametersInput from '$lib/components/custom/stake_parameters_input.svelte';
	import Button from '$lib/components/ui/button/button.svelte';

	import type { Keplr } from '@keplr-wallet/types';
	import { connect_stargate_client, create_client, get_validator_data, type NetworkSettings, type ReadClient } from '$lib/network-utils';
	import type { EvalDecentralisationPayload, EvalDecentralisationResponse, StakingResponse, Validator } from '$lib/types/pytypes';
	import NetworkInfo from '$lib/components/custom/network_info.svelte';

	import { VALIDATORS_DATA } from '$lib/stores/ValidatorsData.js';
	import { NETWORK_YIELD, DECENTRALIZATION_RATIO } from '$lib/stores/NetworkState.js';
	import { FAKE_VALIDATORS } from '$lib/debug/data.js';
	import { READ_CLIENT, STARGATE_SIGNING_CLIENT, WRITE_CLIENT } from '$lib/stores/Clients.js';

	let staking_response: StakingResponse | null = null;


	let isLocalhost = window.location.hostname === 'localhost';

	export let data;

	let network_settings: NetworkSettings = data.network_settings;
	onMount(async () => {
		//let network_settings: NetworkSettings = data.network_settings;
		READ_CLIENT.set(await create_client(data.network_settings.rpc));
		//await connect_stargate_client(network_settings);


		if (isLocalhost) {
			console.log("running in localhost")
		}
		
		
		try {
			VALIDATORS_DATA.set(await get_validator_data($READ_CLIENT!));
		} catch (e) {
			console.log(e)
		}
		/*
		VALIDATORS_DATA.set(
			FAKE_VALIDATORS
		);
		*/
		
		
		// TODO: pass validators data to the api call for eval
		try {
			/*
			let payload: EvalDecentralisationPayload = {
				stakes: [2580, 38000, 12500],
				total_supply: 72000
			}
			*/
			let stakes = $VALIDATORS_DATA.map(
				(val: Validator) => {
					return val.curr_stake
				}
			);

			let payload: EvalDecentralisationPayload = {
				stakes: stakes,
				total_supply: 0.0
			}

			let decentralisation_res = await fetch(
				"/api/eval", //-decentralisation",
				{
					method: "POST",
					headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json'
					},
					body: JSON.stringify(payload)
				}
			)

			let rslt: EvalDecentralisationResponse = await decentralisation_res.json()

			DECENTRALIZATION_RATIO.set(
				rslt.decentralisation_ratio
			);

		} catch (e) {
			console.log(e)
		}

	})
</script>

<svelte:head>
	<title>Cosmos Stake Optimizer</title>
</svelte:head>

<div class="bg-primary">
	<div class="m-auto max-w-4xl h-screen py-16">
		<div class="grid grid-cols-1 gap-24 place-content-between">
			<!-- // TODO: add query network yield -->
			<NetworkInfo nb_validators={$VALIDATORS_DATA.length} network_yield={$NETWORK_YIELD} decentralisation_ratio={$DECENTRALIZATION_RATIO} />
			<div class="w-full">
				<div
					class="grid grid-rows gap-8 border border-2 p-8 w-full rounded-lg bg-primary-foreground"
				>
					<div>
						<div class="grid grid-cols-3">
							<div class="col-span-2">
								<h1 class="font-semibold text-lg">Stake Optimizer</h1>
								<p class="text-gray-400">Maximize yield when staking and help decentralise governance</p>
							</div>
							<div class="col-span-1 grid place-items-end">
								<div class="pb-4">
									{#if $STARGATE_SIGNING_CLIENT}
										<Button class="" variant="outline" on:click={() => {STARGATE_SIGNING_CLIENT.set(null)}}
											>Disconnect</Button
										>
									{:else}
										<Button class="" on:click={async () => {
											//WRITE_CLIENT.set(await connect_stargate_client(network_settings))
											await connect_stargate_client(network_settings);
										}}>Connect Wallet</Button>
									{/if}
								</div>
							</div>
						</div>
						<Separator />
					</div>

					<div class="w-full">
						<StakeParametersInput />
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
