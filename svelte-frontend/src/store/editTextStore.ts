import { writable } from 'svelte/store';

export interface EditLayerState {
    isActive: boolean;
}

function createEditLayerStore() {
    const { subscribe, set, update } = writable<EditLayerState>({
        isActive: false
    });

    return {
        subscribe,
        toggle: () => {
            update(state => {
                console.log('Edit layer state changed:', { ...state, isActive: !state.isActive });
                return { ...state, isActive: !state.isActive };
            });
        },
        reset: () => {
            console.log('Edit layer state reset');
            set({ isActive: false });
        }
    };
}

export const editLayerStore = createEditLayerStore(); 