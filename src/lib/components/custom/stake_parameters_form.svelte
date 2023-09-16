<script lang="ts">
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import InputBalance from '../ui/input_balance/input_balance.svelte';

	import { STAKE_API_RES_STORE, stake_opt_params_store } from '$lib/stores/StakeData';
	import { FAKE_VALIDATORS, FAKE_VALIDATORS_API_RESP } from '$lib/debug/data';
	import type { StakeOptimizePayload, StakeOptimizeResponse } from '$lib/types/pytypes';
	import { VALIDATORS_DATA } from '$lib/stores/ValidatorsData';

	async function optimize_stake() {
		let amount_to_stake = $stake_opt_params_store.amount_to_stake;
		let profit_priority = $stake_opt_params_store.profit_priority;

		let payload: StakeOptimizePayload = {
			total_supply: 0.0,
			amount_to_stake: parseFloat(amount_to_stake),
			yield_prority: profit_priority,
			validator_set: $VALIDATORS_DATA
		};

		console.log(payload.amount_to_stake)


		try {
			const response = await fetch('/api/optimize', {
				method: 'POST',
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});
			let staking_response: StakeOptimizeResponse = await response.json();
			console.log(staking_response);

			STAKE_API_RES_STORE.set(
				staking_response
			);
		} catch (e) {
			console.log(`optimisation failed with error: ${e}`)
		}

	}
</script>

<form class="grid grid-cols-1 gap-2" on:submit={optimize_stake}>
	<div class="w-full">
		<Label for="amount_to_stake">Amount to stake</Label>
		<InputBalance
			name={'amount_to_stake'}
			required={true}
			pattern="\d+\.?\d*"
			placeholder="0.0"
			id="amount_to_stake"
			class="max-w-xs"
			bind:value={$stake_opt_params_store.amount_to_stake}
		/>
	</div>
	<div class="w-full">
		<!--
		<Label for="yield_priority"
			>Profit Priority %
			<Tooltip.Root>
				<Tooltip.Trigger>(?)</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Determine whether to maximize network decentralisation or maxime your yield.</p>
					<p>
						A value of 0 prioritises network decentralisation while a value of 100 maximises yield.
					</p>
				</Tooltip.Content>
			</Tooltip.Root></Label
		>
		<Input
			type="number"
			placeholder="0.0"
			max="100"
			min="0"
			id="yield_priority"
			class="max-w-xs"
			bind:value={$stake_opt_params_store.profit_priority}
		/>
	-->
	</div>
	<div class="w-full py-4">
		<Button class="w-full">Compute Optimal Stake</Button>
	</div>
</form>
