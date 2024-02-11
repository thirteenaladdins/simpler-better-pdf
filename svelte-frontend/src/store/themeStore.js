import { writable } from 'svelte/store';

function getInitialTheme() {
	if (typeof window !== 'undefined') {
		const storedTheme = localStorage.getItem('theme');
		const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
			? 'dark'
			: 'light';

		if (storedTheme) {
			// If 'system' is stored, apply system preference
			return storedTheme === 'system'
				? { selected: 'system', actual: systemTheme }
				: { selected: storedTheme, actual: storedTheme };
		}

		// Default when no theme is stored
		return { selected: 'system', actual: systemTheme };
	}

	// Default for SSR
	return { selected: 'light', actual: 'light' };
}

const initialTheme = getInitialTheme();
export const theme = writable(initialTheme);

theme.subscribe((currentTheme) => {
	if (typeof window !== 'undefined') {
		localStorage.setItem('theme', currentTheme.selected);
	}
});
