<script>
	import { selectedItem } from '../store/selectedItemStore.js';
	import { theme } from '../store/themeStore.js';

	import Moon from '../icons/moon.svelte';
	import Sun from '../icons/sun.svelte';
	import Serpent from '../icons/serpent.svelte';
	import Settings from '../icons/settings.svelte';

	function toggleHighlight(itemName) {
		if ($selectedItem !== itemName) {
			selectedItem.set(itemName);
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
			console.log('theme', $theme.actual);
			document.documentElement.setAttribute('data-theme', $theme.actual);
		}
	}
</script>

<div class="sidenav">
	<span class="sidebar-title font-sans">TOOLS</span>

	<button
		on:click={() => toggleHighlight('ALS Header New')}
		class="sidebar-button font-sans {$selectedItem === 'ALS Header' ? 'on-selected-sidebar' : ''}"
	>
		ALS Header
	</button>
	<button
		on:click={() => toggleHighlight('ALS Header 2')}
		class="sidebar-button font-sans {$selectedItem === 'ALS Header 2' ? 'on-selected-sidebar' : ''}"
	>
		ALS Header 2
	</button>

	<div class="theme-button-container">
		<button
			on:click={() => toggleHighlightTheme('light')}
			class="sidebar-button font-sans {$theme.selected === 'light' ? 'on-selected-sidebar' : ''}"
		>
			<Sun />
		</button>
		<button
			on:click={() => toggleHighlightTheme('dark')}
			class="sidebar-button font-sans {$theme.selected === 'dark' ? 'on-selected-sidebar' : ''}"
		>
			<Moon />
		</button>
		<button
			on:click={() => toggleHighlightTheme('system')}
			class="sidebar-button font-sans {$theme.selected === 'system' ? 'on-selected-sidebar' : ''}"
		>
			<Settings />
		</button>

		<button
			on:click={() => toggleHighlightTheme('serpent')}
			class="sidebar-button font-sans {$theme.selected === 'serpent' ? 'on-selected-sidebar' : ''}"
		>
			<Serpent />
		</button>
	</div>
</div>

<style>
	/* Small devices (landscape phones, 576px and up) */
	/* @media only screen and (max-width: 576px) {  
  .sidebar-list {
    display: flex;
    align-items: center;
    justify-content: center;
  }
} */

	/* Medium devices (tablets, 768px and up) The navbar toggle appears at this breakpoint */
	/* @media (min-width: 768px) {
  
} */

	/* Large devices (desktops, 992px and up) */
	/* @media only screen and (min-width: 992px) {
} */

	/* Extra large devices (large desktops, 1200px and up) */
	/* @media (min-width: 1200px) {} */

	.font-sans {
		font-family: system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue,
			Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol,
			Noto Color Emoji;
	}

	.sidenav {
		display: flex;
		padding-top: 16px;
		width: 126px;
		/* background-color: #E7491D; */
		/* background-color: rgb(255, 117, 4); */
		/* border-right: 1px solid black; */
		flex-direction: column; /* Stacks children vertically */
		/* justify-content: space-between;  */
		height: 100%; /* Use 100% of the parent's height */
		overflow: auto;
		border-right: 2px solid;
		border-right-color: var(--accent-color);
	}

	/* Centering text inside .sidebar-button */
	.sidebar-button {
		/* ... (your existing styles inside this class) ... */
		line-height: 36px;
	}

	/* Style the settings button similar to .sidebar-button */
	.sidenav button {
		display: inline-block;
		list-style: none;
		border: 1px solid transparent;
		border-radius: 4px;
		/* background-color: transparent; */
		background-color: transparent;
		padding: 0 10px;
		margin: 4px;
		/* margin-top: 10px; */
		/* min-width: 8rem; */
		/* height: 36px; */
		line-height: 36px;
		vertical-align: middle;
		/* text-align: center; */
		/* background-color: #fff; */
		color: var(--text-color);
		font-size: 14px;
		font-weight: 400;
		cursor: pointer;
		transition: box-shadow 0.2s;
		text-decoration: none; /* To remove the underline from the anchor tag */
		display: flex;
		justify-content: left;
		align-items: center; /* center vertically */
	}

	.sidenav button:hover {
		color: var(--active-text-color);
	}

	.sidebar-title {
		font-size: 0.75rem;
		padding: 0 10px;
		margin: 4px;
		color: rgb(167, 175, 215);
	}

	/* if sidebar links clicked */
	.sidenav button.on-selected-sidebar {
		/* background-color: rgb(225, 232, 240); */
		border: 1px solid transparent;
		color: var(--active-text-color);
		font-weight: 500;
	}

	.theme-button-container {
		display: flex;
		width: 100%;
		flex-wrap: wrap;
		margin-top: auto;
		margin-bottom: 10px;
	}

	.theme-button-container button {
		padding: 10px;
		border: 1px solid transparent;
	}

	.theme-button-container button:hover {
		padding: 10px;
		color: var(--active-text-color);
		border: 1px solid var(--active-text-color);
	}

	.theme-button-container button.on-selected-sidebar {
		border: 1px solid var(--active-text-color);
	}

	.disabled-icon {
		filter: grayscale(100%);
		opacity: 0.6; /* Optional: to reduce the opacity for a more "disabled" look */
		pointer-events: none; /* Disables any mouse interactions */
		cursor: not-allowed; /* Indicates the item is not clickable */
	}
</style>
