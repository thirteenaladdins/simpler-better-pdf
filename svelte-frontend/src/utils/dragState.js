import { writable } from 'svelte/store';

export const isHighlighted = writable(false);

// export let isHighlighted = writable(false);
export let dragCounter = 0;

// export function setHighlight(value) {
// 	isHighlighted = value;
// }

export function setHighlight(value) {
	if (dragCounter === 0 || value) {
		// set state here
		isHighlighted.set(value);
	}
}

export function increaseCounter() {
	dragCounter++;
	setHighlight(true);
}

export function decreaseCounter() {
	dragCounter--;
	if (dragCounter === 0) {
		setHighlight(false);
	}
}

export function resetCounter() {
	dragCounter = 0;
	setHighlight(false);
}
