from _types import StakeOptimizePayload
from _optimizer import stake_optimize


# need to adjust imports to run this
if __name__ == "__main__":
    with open("stake_payload.json", "r") as f:
        data = f.read()
    
    payload = StakeOptimizePayload.from_json(data)
    payload.amount_to_stake = 1.0
    print([v.curr_stake for v in payload.validator_set])
    weights = stake_optimize(payload.amount_to_stake, payload.validator_set)
    print(weights)