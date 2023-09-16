import type { Validator } from '$lib/types/pytypes';
import { writable, type Writable } from 'svelte/store';


export const VALIDATORS_DATA: Writable<Validator[]> = writable([]);
