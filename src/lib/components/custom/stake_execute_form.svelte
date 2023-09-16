<script lang="ts">
	import Label from '$lib/components/ui/label/label.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Tooltip from '$lib/components/ui/tooltip';

	import { STAKE_API_RES_STORE } from '$lib/stores/StakeData';
	import { STARGATE_SIGNING_CLIENT, USER_ADDRESS, WRITE_CLIENT } from '$lib/stores/Clients';
	import { MsgDelegate } from 'cosmjs-types/cosmos/staking/v1beta1/tx';
	import type { MsgDelegateEncodeObject } from '@cosmjs/stargate';
	import { HACKATHON_MEMO } from '$lib/network-utils';
	import toast from 'svelte-french-toast';
	import { COSMOS_TESTNET } from '$lib/settings/cosmos_testnet';

	const network_settings = COSMOS_TESTNET;

	function value_to_coin_amount(value: number): string {
		return (value * Math.pow(10, network_settings.token.decimals)).toFixed(0);
	}

	async function execute_stakings() {
		const stakingMessages = $STAKE_API_RES_STORE!.targets
			.map((target) =>
				MsgDelegate.fromPartial({
					amount: {
						amount: value_to_coin_amount(target.amount_to_stake),
						denom: "uatom"
					}, // target.amount_to_stake, // need to change to coin and modify amount
					delegatorAddress: $USER_ADDRESS!,
					validatorAddress: target.address
				})
			)
			.map((elem) => ({
				typeUrl: '/cosmos.staking.v1beta1.MsgDelegate',
				value: elem
			}));

		const stakingTx = $STARGATE_SIGNING_CLIENT!.signAndBroadcast(
			$USER_ADDRESS!,
			stakingMessages,
			'auto',
			HACKATHON_MEMO
		);

		toast.promise(stakingTx, {
			loading: 'Sending Transaction...',
			success: (val) => {
				return `Success!\n Hash: ${val.transactionHash}`;
			},
			error: (err) => {
				return `Something went wrong.\n ${(err as Error).message}`;
			}
		});

		stakingTx.then();
	}
</script>

<div class="grid grid-cols-1 justify-end gap-2">
	<div class="w-full">
		<!--
		<Label
			>Expected Yield <Tooltip.Root>
				<Tooltip.Trigger>(?)</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Network yield adjusted by validators commission</p>
				</Tooltip.Content>
			</Tooltip.Root></Label
		>
		<p class="text-foreground">
			{#if $STAKE_API_RES_STORE}
				{($STAKE_API_RES_STORE.expected_yield * 100.0).toFixed(2)}%
			{:else}
				NA
			{/if}
		</p>
		-->
	</div>
	<div class="w-full">
		<Label>Expected Decentralisation Ratio</Label>
		<p class="text-foreground">
			{#if $STAKE_API_RES_STORE}
				{((1.0 - $STAKE_API_RES_STORE.decentralisation_ratio) * 100.0).toFixed(2)}%
			{:else}
				NA
			{/if}
		</p>
	</div>
	<div class="w-full py-4">
		<Button class="w-full" disabled={!$STAKE_API_RES_STORE || !$STARGATE_SIGNING_CLIENT} on:click={async () => {await execute_stakings()}}
			>{!$STARGATE_SIGNING_CLIENT
				? 'Wallet Not Connected'
				: $STAKE_API_RES_STORE
				? 'Execute Stake'
				: 'Stake Not Optimized'}</Button
		>
	</div>
</div>
