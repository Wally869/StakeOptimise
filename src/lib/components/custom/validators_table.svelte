<script lang="ts">
	import * as Table from '$lib/components/ui/table';

	import { STAKE_API_RES_STORE } from '$lib/stores/StakeData';
    
</script>

<Table.Root class="">
	<Table.Caption>Stake will be allocated to the following validators</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="">Validator Name</Table.Head>
			<!--<Table.Head>Validator Address</Table.Head>-->
			<Table.Head class="text-right">Amount to stake</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#if $STAKE_API_RES_STORE}
			{#each $STAKE_API_RES_STORE.targets as validator_res}
				<Table.Row>
					<Table.Cell class="font-medium">{validator_res.moniker}</Table.Cell>
					<!--<Table.Cell>{validator_res.address}</Table.Cell>-->
					<Table.Cell class="text-right">{validator_res.amount_to_stake}</Table.Cell>
				</Table.Row>
			{/each}
		{/if}
	</Table.Body>
</Table.Root>
