<script lang="ts">
	import * as Table from '$lib/components/ui/table';

	export let network_yield: number | null = 0.075;
	export let nb_validators: number | null = 75;
	export let decentralisation_ratio: number | null = 0.75;
</script>

<div
	class="border border-2 rounded-lg w-full max-w-lg grid grid-cols-1 gap-2 mx-auto p-2 bg-primary-foreground"
>
	<h2 class="font-semibold text-center">Network Info</h2>
	<Table.Root class="table-fixed">
		<Table.Header>
			<Table.Row>
				<Table.Head class="text-center">Current Yield</Table.Head>
				<Table.Head class="text-center">Validators Count</Table.Head>
				<Table.Head class="text-center">Decentralisation Ratio</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			<Table.Row>
				<Table.Cell class="text-center text-foreground"
					>{network_yield ? `${(network_yield * 100.0).toFixed(2)}%` : 'Loading...'}</Table.Cell
				>
				<Table.Cell class="text-center text-foreground">{nb_validators ? nb_validators : "Loading..."}</Table.Cell>
				<Table.Cell class="text-center text-foreground"
					>{decentralisation_ratio ? `${((1.0 - decentralisation_ratio) * 100.0).toFixed(2)}%` : "Loading..."}</Table.Cell
				>
			</Table.Row>
		</Table.Body>
	</Table.Root>
</div>
