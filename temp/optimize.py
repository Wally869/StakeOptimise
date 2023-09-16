from http.server import BaseHTTPRequestHandler
from datetime import datetime

import numpy as np
import json

from .types import StakingResponse, StakingTarget

from random import choices, seed, random
import string


NB_VALIDATORS = 5
ADDRESS_LENGTH = 18
MAX_VAL = 10000

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.end_headers()

        resp = StakingResponse([
            StakingTarget(
                address=''.join(
                    choices(string.ascii_uppercase + string.digits, k=ADDRESS_LENGTH)
                ),
                amount_to_stake=random() * MAX_VAL
            ) for _ in range(NB_VALIDATORS)
        ])

        self.wfile.write(
            json.dumps(resp.to_dict()).encode()
        )

        
        """
        self.wfile.write(
            json.dumps(
                {
                    "data": np.random.random(10).tolist()
                }
            ).encode()
        )
        """

        return
    