// Generated using py-ts-export interfaces.
// See https://github.com/cs-cordero/py-ts-export interfaces

export interface Validator {
    moniker: string;
    address: string;
    curr_stake: number;
    commission_rate: number;
}

export interface StakingData {
    total_supply: number;
    amount_to_stake: number;
    validator_set: Array<Validator>;
}

export interface StakeOptimizePayload {
    total_supply: number;
    amount_to_stake: number;
    yield_prority: number;
    validator_set: Array<Validator>;
}

export interface StakingTarget {
    moniker: string;
    address: string;
    amount_to_stake: number;
}

export interface StakingResponse {
    expected_yield: number;
    targets: Array<StakingTarget>;
}

export interface StakeOptimizeResponse {
    expected_yield: number;
    decentralisation_ratio: number;
    targets: Array<StakingTarget>;
}

export interface EvalDecentralisationPayload {
    stakes: Array<number>;
    total_supply: number;
}

export interface EvalDecentralisationResponse {
    decentralisation_ratio: number;
}
