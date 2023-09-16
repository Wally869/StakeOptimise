import { writable, type Writable } from 'svelte/store';

export interface INetworkState {
    current_yield: number
    validators_count: number
    decentralisation_ration: number
}

export const network_state_store: Writable<null | INetworkState>  = writable(null);


export const NETWORK_YIELD: Writable<number> = writable(0);

export const DECENTRALIZATION_RATIO: Writable<number> = writable(0);