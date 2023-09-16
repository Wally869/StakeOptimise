import type { StakeOptimizeResponse } from '$lib/types/pytypes';
import { writable, type Writable } from 'svelte/store';

export interface IStakeOptParams {
    amount_to_stake: string
    profit_priority: number
}

export const stake_opt_params_store: Writable<IStakeOptParams> = writable({ amount_to_stake: "0.0", profit_priority: 50.0 });


export interface ValidatorStakeToAdd {
    moniker: string
    address: string
    amount_to_stake: number
}

/*
export interface IStakeApiResponse {
    expected_yield: number
    expected_decentralisation_ratio: number
    validators: ValidatorStakeToAdd[]
}
*/

export const STAKE_API_RES_STORE: Writable<StakeOptimizeResponse | null> = writable(null);

