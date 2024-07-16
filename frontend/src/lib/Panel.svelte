<script lang="ts">
	import { createEventDispatcher } from "svelte";

	import { ChosePointState } from "./enums";
	import type { Point } from "./types";

	const dispatch = createEventDispatcher();

	export let point1: Point;
	export let point2: Point;
	export let chosingPointState: ChosePointState;
	export let polyCount: number;

	let hidden = false;

	const toggle = () =>
		hidden = !hidden;

	const update = () =>
		dispatch("update");

	interface PointInput {
		lat: number;
		lng: number;
	}

	const selectPoint = (state: ChosePointState) => {
		if (chosingPointState === state)
			state = ChosePointState.Standby;

		chosingPointState = state;
	}

	const pointInput1: PointInput = {
		lat: 0,
		lng: 0
	};
	const pointInput2: PointInput = {
		lat: 0,
		lng: 0
	};

	const updatePointsFromInput = () => {
		point1 = [pointInput1.lat, pointInput1.lng];
		point2 = [pointInput2.lat, pointInput2.lng];
	}

	const updateInputFromPoints = () => {
		pointInput1.lat = point1[0];
		pointInput1.lng = point1[1];
		pointInput2.lat = point2[0];
		pointInput2.lng = point2[1];
	}

	$: point1, point2, updateInputFromPoints();
</script>

<!-- class:dark={mapMode === MapMode.Dark || mapMode === MapModes.Satelite} -->
<div class="panel" class:hidden>
	<div class="handle"
		on:click={toggle}
		on:keydown={e => e.key === "Enter" && toggle()}

		role="button"
		tabindex="0"
		>⣿</div>
	<div class="content">
		<div class="group">
			<h3>Точка 1</h3>
			<button on:click={() => selectPoint(ChosePointState.ChosingPoint1)} class:active={chosingPointState === ChosePointState.ChosingPoint1}>📌 На карте</button>
			<div class="field">
				<span>Широта</span>
				<input type="number" min="-90" max="90" bind:value={pointInput1.lat} on:change={updatePointsFromInput}>
			</div>
			<div class="field">
				<span>Долгота</span>
				<input type="number" min="-180" max="180" bind:value={pointInput1.lng} on:change={updatePointsFromInput}>
			</div>
		</div>
		<div class="group">
			<h3>Точка 2</h3>
			<button on:click={() => selectPoint(ChosePointState.ChosingPoint2)} class:active={chosingPointState === ChosePointState.ChosingPoint2}>📌 На карте</button>
			<div class="field">
				<span>Широта</span>
				<input type="number" min="-90" max="90" bind:value={pointInput2.lat} on:change={updatePointsFromInput}>
			</div>
			<div class="field">
				<span>Долгота</span>
				<input type="number" min="-180" max="180" bind:value={pointInput2.lng} on:change={updatePointsFromInput}>
			</div>
		</div>
		<div class="group">
			<!-- Slider -->
			<h3>Количество полигонов</h3>
			<div class="field">
				<span>{polyCount}</span>
				<input type="range" min="1" max="100" bind:value={polyCount} on:change={updatePointsFromInput}>
			</div>
		</div>
		<button class="submit" on:click={update}>🚀 Отправить 🚀</button>
	</div>
</div>

<style>
	:root {
		--width: 340px;
		--handle-width: 25px;
	}

	.panel {
		/* Игра с цветами */
		--main-color: #0f0f0f;
		--handle-color: #292929;
		--interactive-color: #313131;
		--active-color: #361e1e;
		--enabled-color: #fff;
		
		position: absolute;
		top: 20px;
		right: 0;
		width: var(--width);
		
		display: flex;
		flex-direction: row;

		color: #fff;
		background-color: var(--main-color);
		border-radius: 8px 0 0 8px;

		font-family: Arial, Helvetica, sans-serif;

		transition: .3s ease-in-out;

		overflow: hidden;
	}

	/* .panel.dark {
		--main-color: #0f0f0f;
		--handle-color: #292929;
		--interactive-color: #313131;
		--active-color: #361e1e;
		--enabled-color: #fff;
	} */

	.handle {
		width: var(--handle-width);

		background-color: var(--handle-color);

		display: flex;
		justify-content: center;
		align-items: center;

		flex-shrink: 0;

		cursor: pointer;
	}

	.panel.hidden {
		transform: translateX(calc(var(--width) - var(--handle-width)));
	}


	.content {
		width: 100%;
		padding: 20px;

		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.content button {
		background: var(--interactive-color);
		color: #fff;

		padding: 5px 10px;
		border-radius: 3px;

		border: none;

		transition: .1s;
	}

	.content button:hover {
		filter: brightness(1.2);
	}

	.content button:active {
		filter: brightness(0.9);
		transform: scale(0.99);
	}

	.content button.active {
		background: var(--active-color);
	}

	.group {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	.group .field {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 10px;
	}

	.group .field span {
		min-width: 30px;
		text-align: right;
	}

	.group .field input[type="number"] {
		flex-grow: 1;

		width: 180px;
		padding: 5px 10px;
		border-radius: 3px;

		background: var(--interactive-color);
		color: #fff;

		border: none;

		transition: .1s;
	}

	.group .field input[type="number"]:focus {
		outline: none;
		/* filter: brightness(1.2); */
		background-color: var(--active-color);
	}

	.group .field input[type="range"] {
		flex-grow: 1;

		appearance: none;

		height: 16px;
		border-radius: 3px;

		background: var(--interactive-color);
		outline: none; 
		
		transition: .2s;
	}

	.group .field input[type="range"]::-webkit-slider-thumb {
		appearance: none;

		width: 20px;
		height: 15px;
		border-radius: 3px;

		background: var(--enabled-color);

		cursor: pointer;
	}

	.group .field input[type="range"]::-moz-range-thumb {
		width: 20px;
		height: 15px;
		border-radius: 3px;

		background: var(--enabled-color);

		cursor: pointer;
	}
</style>