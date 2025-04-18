<script>
	import { selectedItem } from '../store/selectedItemStore.js';
	import { theme } from '../store/themeStore.js';
	import { editLayerStore } from '../store/editTextStore.js';
	import Serpent from '../icons/serpent.svelte';
	import { TypeIcon, SunIcon, MoonIcon, SettingsIcon } from 'svelte-feather-icons';

	function toggleHighlight(itemName) {
		if ($selectedItem !== itemName) {
			selectedItem.set(itemName);
			if (itemName === 'edit text') {
				editLayerStore.toggle();
			}
		}
	}

	function toggleHighlightTheme(themeName) {
		theme.set({ selected: themeName, actual: themeName });
	}

	let isNavOpen = false;
	let showTools = true;
	let isDarkMode = false;

	// Reactively update the data-theme attribute
	$: {
		if (typeof window !== 'undefined' && $theme) {
			document.documentElement.setAttribute('data-theme', $theme.actual);
		}
	}
</script>

<div class="sidenav font-sans">
	<span class="sidebar-title">TOOLS</span>

	<div class="tool-container">
		<button
			on:click={() => {
				toggleHighlight('edit text');
				editLayerStore.toggle();
			}}
			class="sidebar-button {$editLayerStore.isActive ? 'on-selected-sidebar' : ''}"
		>
			<TypeIcon size="24" />
		</button>
	</div>

	<span class="sidebar-title">LEGACY TOOLS</span>

	<button
		on:click={() => toggleHighlight('ALS Header')}
		class="sidebar-button {$selectedItem === 'ALS Header' ? 'on-selected-sidebar' : ''}"
	>
		ALS Header
	</button>
	<button
		on:click={() => toggleHighlight('ALS Header 2')}
		class="sidebar-button {$selectedItem === 'ALS Header 2' ? 'on-selected-sidebar' : ''}"
	>
		ALS Header 2
	</button>

	<span class="sidebar-title">THEMES</span>

	<div class="theme-button-container">
		<button
			on:click={() => toggleHighlightTheme('light')}
			class="sidebar-button {$theme.selected === 'light' ? 'on-selected-sidebar' : ''}"
		>
			<SunIcon />
		</button>
		<button
			on:click={() => toggleHighlightTheme('dark')}
			class="sidebar-button {$theme.selected === 'dark' ? 'on-selected-sidebar' : ''}"
		>
			<MoonIcon />
		</button>
		<button
			on:click={() => toggleHighlightTheme('serpent')}
			class="sidebar-button {$theme.selected === 'serpent' ? 'on-selected-sidebar' : ''}"
		>
			<Serpent />
		</button>
		<button
			on:click={() => toggleHighlightTheme('system')}
			class="sidebar-button {$theme.selected === 'system' ? 'on-selected-sidebar' : ''}"
		>
			<SettingsIcon />
		</button>
	</div>
</div>

<style>
	/***** BASE FONT *****/
	.font-sans {
		font-family:
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			Segoe UI,
			Roboto,
			Helvetica Neue,
			Arial,
			Noto Sans,
			sans-serif,
			Apple Color Emoji,
			Segoe UI Emoji,
			Segoe UI Symbol,
			Noto Color Emoji;
	}

	/***** SIDENAV CONTAINER *****/
	.sidenav {
		/* Layout */
		display: flex;
		flex-direction: column;
		/* 
		  If you want this to be more of a sidebar:
		  width: 240px;
		  or 100% if it's part of a mobile layout.
		*/
		padding: 16px;
		margin: 0 auto; /* Center horizontally if you want, else remove or adjust */

		/* Visuals */
		border: 2px solid var(--accent-color);
		border-radius: 10px;
		background-color: transparent; /* or var(--bg-color) if you want a background */

		/* Gap for spacing between child elements (modern browsers) */
		gap: 16px;
		width: fit-content; /* Shrinks container to its content's width */
	}

	/***** HEADINGS / TITLES *****/
	.sidebar-title {
		font-size: 0.75rem;
		color: rgb(167, 175, 215);
		margin: 0; /* Reset default heading margins */
	}

	/***** TOOL & THEME CONTAINER *****/
	.tool-container,
	.theme-button-container {
		display: flex;
		flex-wrap: wrap;
		/* Creates spacing between buttons in modern browsers */
		gap: 8px;
	}

	/***** BUTTON STYLES *****/
	/* The .sidebar-button class can hold most of your shared button styles */
	.sidebar-button {
		display: flex;
		align-items: center;
		justify-content: center; /* or left if you prefer icons left-aligned */
		gap: 8px; /* space between icon & text if you have text in future */

		/* Spacing inside the button */
		padding: 8px 12px;

		/* Visuals */
		font-size: 14px;
		font-weight: 400;
		color: var(--text-color);
		background-color: transparent;
		border: 1px solid var(--accent-color);
		border-radius: 4px;
		cursor: pointer;
		transition:
			background-color 0.2s,
			color 0.2s,
			border-color 0.2s;
	}

	/* Hover state */
	.sidebar-button:hover {
		color: var(--active-text-color);
		border-color: var(--active-text-color);
	}

	/***** SELECTED STATE *****/
	.sidebar-button.on-selected-sidebar {
		border-color: var(--accent-color);
		font-weight: 500;
		background-color: var(--button-bg-color);
		/* color: var(--text-color); */
		color: #fff;
	}

	/***** ANY EXTRA STATES (FOCUS, ACTIVE, ETC.) *****/
	/* .sidebar-button:focus {
		outline: none;
		box-shadow: 0 0 0 2px var(--accent-color);
	} */
</style>
