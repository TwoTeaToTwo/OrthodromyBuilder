<script lang="ts">
	import { onMount } from "svelte";

	import { requestPoints } from "$lib/API";
	import { ChosePointState } from "$lib/enums";
	import type { Point } from "$lib/types";

	import Map from "$lib/Map.svelte";
	import Panel from "$lib/Panel.svelte";
	
	let points: Point[] = [];

	let point1: Point = [55, 37];
	let point2: Point = [23, -82];

	let chosingPointState: ChosePointState = ChosePointState.Standby;
	let polyCount: number = 10;

	const update = async () => 
		points = await requestPoints(point1, point2, polyCount);

	onMount(update);
</script>

<svelte:head>
	<title>Построение ортодрома</title>
</svelte:head>

<Map bind:points bind:point1 bind:point2 bind:chosingPointState/>
<Panel bind:point1 bind:point2 bind:chosingPointState bind:polyCount on:update={update}/>

<style>

</style>