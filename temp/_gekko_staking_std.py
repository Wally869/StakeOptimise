from gekko import GEKKO
import numpy as np
from typing import List
from typing_extensions import Self
from dataclasses import dataclass

from random import random, choices, seed
import string

ADDRESS_LENGTH = 18
MAX_DELEGATED = 100000000.0
MAX_COMMISSION_RATE = 0.2

NB_VALIDATORS = 75
NAKAMOTO_THRESHOLD = 0.33

YIELD = 0.15

AMOUNT_IN = 200000000.0


seed(42069)


@dataclass
class Validator:
    address: str
    staked_amount: float
    commission_rate: float

    @classmethod
    def random(cls) -> Self:
        return Validator(
            address=''.join(choices(string.ascii_uppercase +
                            string.digits, k=ADDRESS_LENGTH)),
            staked_amount=random() * MAX_DELEGATED,
            commission_rate=round(random() * MAX_COMMISSION_RATE, 3)
        )


validator_set: List[Validator] = [
    Validator.random() for _ in range(NB_VALIDATORS)
]

total_supply = sum(validator.staked_amount for validator in validator_set)


# convert supplies to % 
pct_staked = [validator.staked_amount / total_supply for validator in validator_set]


# what is the initial std dev? 
init_std = np.std(pct_staked)
print(f"init std: {init_std}")


m = GEKKO(remote=False)

#m.options.SOLVER = 3
# m.cleanup()
weights = m.Array(m.Var, NB_VALIDATORS, value=1.0 / NB_VALIDATORS, lb=0, ub=1)


m.Equation(m.sum(weights) == 1.0)


# compute temp stakes pct after allocating the amount to stake depending on current weights
temp_stakes = [
    m.Intermediate(
        (validator_set[i].staked_amount + weights[i] * AMOUNT_IN) / (total_supply + AMOUNT_IN),
        name=f"stake_val_pct_{i}"
    ) for i in range(NB_VALIDATORS)
]

# compute mean pct 
mean_pct_stake = m.Intermediate(
    m.sum(temp_stakes) / NB_VALIDATORS,
    name="mean_pct_stake"
)

# compute std deviation  
std_dev = m.Intermediate(
    m.sum(
        [(temp_stakes[i] - mean_pct_stake) ** 2 for i in range(NB_VALIDATORS)]
    ) / NB_VALIDATORS
)

# solve (minimize stdev)
m.Minimize(std_dev)

m.solve(disp=True)
print('Objective: ', m.options.OBJFCNVAL)
print('Solution: ', weights)


# terminal std 
new_stakes = [
    (validator_set[i].staked_amount  + AMOUNT_IN * weights[i][0]) / (total_supply + AMOUNT_IN) for i in range(NB_VALIDATORS) 
]

terminal_std = np.std(new_stakes)


print(f"init std: {init_std}")
print(f"terminal std: {terminal_std}")
print(f"added pct supply: {AMOUNT_IN/total_supply}")

def gini(x: List[float]):
    total = 0
    for i, xi in enumerate(x[:-1], 1):
        total += np.sum(np.abs(xi - x[i:]))
    return total / (len(x)**2 * np.mean(x))

print(f"init gini: {gini(np.array([v.staked_amount for v in validator_set]))}")
print(f"terminal gini: {gini(np.array(new_stakes))}")