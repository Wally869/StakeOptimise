from typing import List
from ._types import EvalDecentralisationPayload, EvalDecentralisationResponse, StakeOptimizePayload, StakeOptimizeResponse, StakingTarget

from ._evaluation import eval_decentralization
from ._optimizer import stake_optimize

from flask import Flask, request

app = Flask(__name__)


@app.route("/api/eval", methods=["POST"])
def eval_decentralisation():
    """
    payload = EvalDecentralisationPayload(
        stakes=request.args.get("stakes"),
        total_supply=request.args.get("total_supply")
    )
    """
    payload: EvalDecentralisationPayload = EvalDecentralisationPayload.from_dict(
        request.get_json())

    resp = EvalDecentralisationResponse(
        eval_decentralization(payload.stakes)  # , payload.total_supply)
    )

    return resp.to_json()  # resp.to_json()


@app.route("/api/optimize", methods=["POST"])
def optimize():
    payload: StakeOptimizePayload = StakeOptimizePayload.from_dict(
        request.get_json()
    )

    # compute weights
    weights = stake_optimize(payload.amount_to_stake, payload.validator_set)

    # compute new stakes
    to_stake_per_val = [
        weights[i] * payload.amount_to_stake for i in range(len(payload.validator_set))]
    new_stakes = [
        payload.validator_set[i].curr_stake + to_stake_per_val[i] for i in range(len(payload.validator_set))
    ]

    # compute our new decentralisation ratio
    decentralisation_ratio = eval_decentralization(new_stakes)

    # recompose for response
    targets: List[StakingTarget] = [
        StakingTarget(
            moniker=payload.validator_set[i].moniker,
            address=payload.validator_set[i].address,
            amount_to_stake=weights[i] * payload.amount_to_stake
        ) for i in range(len(payload.validator_set))
    ]

    # prune validators with 0 to stake
    targets = list(filter(lambda x: x.amount_to_stake > 0, targets))
    # prune validators with < 0.0000001 to stake 
    targets = list(filter(lambda x: x.amount_to_stake > 0.000001, targets))

    # create response obj and return
    resp = StakeOptimizeResponse(
        expected_yield=0.0,
        decentralisation_ratio=decentralisation_ratio,
        targets=targets
    )
    return resp.to_json()
