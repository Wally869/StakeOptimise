<script lang="ts">
	import { onMount } from 'svelte';

	let temp: { data: number[] } | null = null;

	async function call_test() {
		console.log('in call test');
		const response = await fetch('/api/testo');
		temp = await response.json();
	}

	onMount(() => {
		call_test();
	});
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

{#if temp}
	<ul>
		{#each temp.data as d}
			<li>{d}</li>
		{/each}
	</ul>
{/if}
