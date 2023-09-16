from typing import List

from gekko import GEKKO


from _types import Validator, StakingTarget, StakingResponse

def optimize_stake(amount_to_stake: float, total_supply: float, validator_set: List[Validator]) -> StakingResponse:
    # extract some constants 
    nb_validators = len(validator_set)

    # set up optimizer
    m = GEKKO(remote=False)

    # define problem and variables
    # compute temp stakes pct after allocating the amount to stake depending on current weights
    weights = m.Array(m.Var, nb_validators, value=1.0 / nb_validators, lb=0, ub=1)
    temp_stakes = [
        m.Intermediate(
            (validator_set[i].curr_stake + weights[i] * amount_to_stake) / (total_supply + amount_to_stake),
            name=f"stake_val_pct_{i}"
        ) for i in range(nb_validators)
    ]

    # compute mean pct 
    mean_pct_stake = m.Intermediate(
        m.sum(temp_stakes) / nb_validators,
        name="mean_pct_stake"
    )

    # compute std deviation  
    std_dev = m.Intermediate(
        m.sum(
            [(temp_stakes[i] - mean_pct_stake) ** 2 for i in range(nb_validators)]
        ) / nb_validators
    )

    # set up objective and solve
    m.Minimize(std_dev)
    m.solve(disp=True)

    terminal_weights = [
        w[0] for w in weights   
    ]

    outputs = [
        StakingTarget(
            address=validator_set[i],
            amount_to_stake=amount_to_stake * terminal_weights[i]
        ) for i in range(nb_validators)
    ]

    return StakingResponse(
        targets=outputs
    )
