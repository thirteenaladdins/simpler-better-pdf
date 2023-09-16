import { writable } from 'svelte/store';

// The initial theme can be set based on user preferences, localStorage, or default to 'light'.
const initialTheme = (typeof window !== 'undefined' && localStorage.getItem('theme')) || 'Light';
export const theme = writable(initialTheme);

// Subscribe to theme changes and update localStorage
theme.subscribe(currentTheme => {
    if (typeof window !== 'undefined') {
        localStorage.setItem('theme', currentTheme);
    }
});
