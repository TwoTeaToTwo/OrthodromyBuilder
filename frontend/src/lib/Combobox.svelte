<script lang="ts">
    import type { AdvancedOption } from "./types";

    export let value = "";
    export let options: (AdvancedOption | string)[] = [];
</script>

<select bind:value>
    {#each options as option}
        {#if typeof option === "string"}
            <option value={option}>{option}</option>
        {:else}
            <option value={option.value}>{option.label}</option>
        {/if}
    {/each}
</select>

<style>
    select {
        --main-color: #313131;

        background-color: var(--main-color);

        box-sizing: border-box;
        padding: 5px 10px;

        border: 1px solid var(--main-color);
        border-radius: 3px;

        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 20px;
        
        color: #fff;
        appearance: none;
        font-family: Arial, Helvetica, sans-serif;

        transition: .1s;
    }

    select:focus {
        outline: none;
    }

    select:hover {
		filter: brightness(1.2);
	}
</style>