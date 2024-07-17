<script lang="ts">
	import { onMount } from "svelte";

	import { requestPoints } from "$lib/API";
	import { ChosePointState } from "$lib/enums";
	import type { Point, AdvancedOption } from "$lib/types";

	import Map from "$lib/Map.svelte";
	import Panel from "$lib/Panel.svelte";
	
	let points: Point[] = [];

	let point1: Point = [55, 37];
	let point2: Point = [23, -82];

	let chosingPointState: ChosePointState = ChosePointState.Standby;
	let polyCount: number = 10;

	let epsg = getEPSG();
	let current_epsg = "EPSG:4326";

	const update = async () => 
		points = await requestPoints(point1, point2, current_epsg, polyCount);

	onMount(update);

	function getEPSG()
	{
		let epsg: AdvancedOption[] = [];
		const WGS84: AdvancedOption = {value: "EPSG:4326", label: "WGS84"};
		const sk72: AdvancedOption = {value: "EPSG:4284", label: "СК-42"};
		const Mercator: AdvancedOption = {value: "EPSG:3857", label: "Mercator"};
		epsg.push(WGS84);
		epsg.push(sk72);
		epsg.push(Mercator);
		return epsg;
	}
</script>

<svelte:head>
	<title>Построение ортодрома</title>
</svelte:head>

<Map bind:points bind:point1 bind:point2 bind:chosingPointState bind:cs={current_epsg}/>
<Panel bind:point1 bind:point2 bind:chosingPointState bind:polyCount {epsg} bind:current_epsg on:update={update}/>

<style>

</style>