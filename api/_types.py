from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from py_ts_interfaces import Interface


@dataclass_json
@dataclass
class Validator(Interface):
    moniker: str
    address: str
    curr_stake: float
    commission_rate: float


@dataclass_json
@dataclass 
class StakingData(Interface):
    total_supply: float
    amount_to_stake: float
    validator_set: List[Validator]


@dataclass_json
@dataclass 
class StakeOptimizePayload(Interface):
    total_supply: float
    amount_to_stake: float
    yield_prority: float 
    validator_set: List[Validator]


@dataclass_json
@dataclass
class StakingTarget(Interface):
    moniker: str
    address: str
    amount_to_stake: float


@dataclass_json
@dataclass
class StakingResponse(Interface):
    expected_yield: float
    targets: List[StakingTarget]


@dataclass_json
@dataclass
class StakeOptimizeResponse(Interface):
    expected_yield: float
    decentralisation_ratio: float
    targets: List[StakingTarget]



@dataclass_json
@dataclass
class EvalDecentralisationPayload(Interface):
    stakes: List[float]
    total_supply: float


@dataclass_json
@dataclass
class EvalDecentralisationResponse(Interface):
    decentralisation_ratio: float
