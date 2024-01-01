import { writable } from 'svelte/store';

function getInitialTheme() {
	if (typeof window !== 'undefined') {
		const storedTheme = localStorage.getItem('theme');

		if (storedTheme) {
			return { selected: storedTheme, actual: storedTheme };
		}

		const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		const initialTheme = prefersDark ? 'dark' : 'light';
		return { selected: initialTheme, actual: initialTheme };
	}

	return { selected: 'light', actual: 'light' };
}

const initialTheme = getInitialTheme();
export const theme = writable(initialTheme);

// Subscribe to theme changes and update localStorage
theme.subscribe((currentTheme) => {
	if (typeof window !== 'undefined') {
		localStorage.setItem('theme', currentTheme.actual);
	}
});
