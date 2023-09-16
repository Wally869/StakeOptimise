<script lang="ts">
	import * as Table from '$lib/components/ui/table';

	export let network_yield: number = 0.075;
	export let nb_validators = 75;
	export let decentralisation_ratio = 0.75;
</script>

<div class="border border-2 rounded-lg w-full max-w-lg grid grid-cols-1 gap-2 mx-auto p-2 bg-primary-foreground">
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
				<Table.Cell class="text-center text-foreground">{(network_yield * 100.0).toFixed(2)}%</Table.Cell>
				<Table.Cell class="text-center text-foreground">{nb_validators}</Table.Cell>
				<Table.Cell class="text-center text-foreground">{((1.0 - decentralisation_ratio) * 100.0).toFixed(2)}%</Table.Cell>
			</Table.Row>
		</Table.Body>
	</Table.Root>
</div>
