from typing import List

from gekko import GEKKO

if __name__ == "__main__":
    from _types import Validator, StakingTarget, StakingResponse
    from _evaluation import eval_decentralization
else:
    from ._types import Validator, StakingTarget, StakingResponse
    from ._evaluation import eval_decentralization

import numpy as np



def stake_optimize(amount_to_stake: float, validator_set: List[Validator]) -> List[float]:
    # extract some constants
    nb_validators = len(validator_set)
    total_supply = sum(val.curr_stake for val in validator_set)

    # set up optimizer
    m = GEKKO(remote=False)
    m.options.SOLVER = 1
    m.options.RTOL=1e-4
    m.options.OTOL=1e-4
    #m.options.MAX_ITER = 200
    """
    m.solver_options = ['minlp_gap_tol 1.0e-2',\
                    'minlp_maximum_iterations 10000',\
                    'minlp_max_iter_with_int_sol 500']
    """
    #m._path = "C:/Users/William/Documents/Work/Hackatons/AEZ/StakeOptimizer/stake-optimizer/api/logs"

    new_total_supply = total_supply + amount_to_stake
    avg_supply = new_total_supply / nb_validators

    weight_flags = [
        0.0 if (validator.curr_stake > avg_supply) else 1.0 for validator in validator_set
    ]
    #exit()
    # define problem and variables
    # compute temp stakes pct after allocating the amount to stake depending on current weights
    weights = m.Array(m.Var, nb_validators, value=1.0 /
                      nb_validators, lb=0, ub=1)


    stakes = [
        val.curr_stake for val in validator_set
    ]

    temp_stakes = [
        m.Intermediate(
            stakes[i] + weights[i] * amount_to_stake,
            name=f"temp-stake-{i}"
        ) for i in range(nb_validators)
    ]

    # compute sqr distance from mean 
    sqr_distances = [
        m.Intermediate(
            (temp_stakes[i] - avg_supply) ** 2,  #* (temp_stakes[i] - avg_supply)
            name=f"sqr-distances-{i}"
        ) for i in range(nb_validators)
    ]
    
    # force weight == 0 for validators above the equirepartition of stakes
    flagged_weights = [
        m.Intermediate(
            weights[i] * weight_flags[i],
            name=f"flagged-weights-{i}"
        ) for i in range(nb_validators)
    ]

    # weights should sum to 1
    m.Equation(m.sum(flagged_weights) == 1.0)

    g = m.Intermediate(m.sum(sqr_distances), name="sum-sqr-dist")

    m.Minimize(g)
    m.solve(disp=False)

    # weights might not be exactly 1, so force to 1
    terminal_weights = np.array([
        w[0] for w in weights
    ])
    terminal_weights /= sum(terminal_weights)
    # print(terminal_weights)
    return terminal_weights.tolist()


if __name__ == "__main__":
    nb_validators = 180

    from random import random
    validators = [
        Validator(
            f"val-{i}",
            f"{i}",
            random() * 20000.0 + 30000.0,
            random() * 0.1
        ) for i in range(nb_validators)
    ]

    initial_stakes = [val.curr_stake for val in validators]
    gini = eval_decentralization(initial_stakes)

    weights = stake_optimize(5000.0, validators)
    nb_used_validators = 0
    for w in weights:
        if w > 0:
            nb_used_validators += 1
    new_stakes = [
        validators[i].curr_stake + weights[i] * 5000.0 for i in range(nb_validators)
    ]
    # eval new gini
    gini = eval_decentralization(new_stakes)
