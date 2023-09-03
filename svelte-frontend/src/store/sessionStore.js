import { writable } from 'svelte/store';

// This function checks if we're running in a browser environment
function isBrowser() {
    return typeof window !== 'undefined';
}

function getInitialData() {
  if (isBrowser()) {
    const data = sessionStorage.getItem('responseData');
    if (data) {
      return JSON.parse(data);
    }
  }
  return null;
}

export const sessionData = writable(getInitialData());

if (isBrowser()) {
  // Only subscribe to store changes if we're in the browser
  sessionData.subscribe(value => {
    if (value !== null) {
      sessionStorage.setItem('responseData', JSON.stringify(value));
    }
  });
}
