from typing import List, Optional

from . import data
from .client import Client


class ClientManager:
    def __init__(self):
        self.clients: List[Client] = data.clients

    def get_client_by_token(self, token: str) -> Optional[Client]:
        filtered_clients = list(filter(lambda c: c.token == token, self.clients))
        if len(filtered_clients) == 0:
            return None

        return filtered_clients[0]
