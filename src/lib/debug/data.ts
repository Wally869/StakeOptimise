import type { StakingTarget, Validator } from "$lib/types/pytypes"

function makeid(length: number): string {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

export const FAKE_VALIDATORS: Validator[] = [];

for (let i = 0; i < 10; i++) {
    FAKE_VALIDATORS.push(
        {
            moniker: makeid(8),
            address: makeid(32),
            curr_stake: Math.random() * 30000.0 + 20000.0,
            commission_rate: Math.random() * 10.0
        }
    )
}


export const FAKE_VALIDATORS_API_RESP: StakingTarget[] = []

for (let i = 0; i < 10; i++) {
    FAKE_VALIDATORS_API_RESP.push(
        {
            moniker: FAKE_VALIDATORS[i].moniker,
            address: FAKE_VALIDATORS[i].address,
            amount_to_stake: Math.random() * 1200.0
        }
    )
}


