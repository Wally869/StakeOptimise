<script lang="ts">
	import ValidatorsTable from './validators_table.svelte';
	import StakeParametersForm from './stake_parameters_form.svelte';
	import StakeExecuteForm from './stake_execute_form.svelte';
</script>

<div class="grid grid-cols-2 w-full gap-8">
	<div class="grid grid-cols-1 justify-stretch">
		<StakeParametersForm />
		<StakeExecuteForm />		
	</div>
	<div class="">
		<div class="h-96 overflow-scroll">
			<ValidatorsTable />
		</div>
	</div>
</div>
