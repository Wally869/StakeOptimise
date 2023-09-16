from .types import EvalDecentralisationPayload, EvalDecentralisationResponse

from http.server import BaseHTTPRequestHandler
import json

from _evaluation import eval_decentralization

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        resp = EvalDecentralisationResponse(
            eval_decentralization([], 0.0)
        )

        self.wfile.write(
            json.dumps(resp.to_dict()).encode()
        )

        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.end_headers()


        return
