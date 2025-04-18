<!-- ToolsAndTemplates.svelte -->
<script>
	import SideNav from './SideNav.svelte';

	function dispatch(eventName, detail) {
		const event = new CustomEvent(eventName, { detail });
		document.dispatchEvent(event);
	}

	let activeTab = 'tools'; // or 'templates'

	// Example: user picks a logo file
	function onLogoSelected(event) {
		const file = event.target.files[0];
		if (file) {
			// Convert file to array buffer or data URL, dispatch an event
			const reader = new FileReader();
			reader.onload = () => {
				dispatch('insertLogo', { src: reader.result });
			};
			reader.readAsDataURL(file);
		}
	}
</script>

<div class="tools-and-templates">
	<div class="tabs">
		<button on:click={() => (activeTab = 'tools')}>Tools</button>
		<button on:click={() => (activeTab = 'templates')}>Templates</button>
	</div>

	{#if activeTab === 'tools'}
		<div class="tools-tab">
			<!-- Future: insert text, highlight, draw, etc. -->
		</div>
	{:else}
		<div class="templates-tab">
			<p>Select a template or upload a logo:</p>
			<input type="file" accept="image/*" on:change={onLogoSelected} />
			<!-- Predefined logos or stamps could go here -->
		</div>
	{/if}
</div>
<SideNav />

<style>
	.tools-and-templates {
		padding: 1rem;
	}
	.tabs button {
		margin-right: 1rem;
	}
</style>
