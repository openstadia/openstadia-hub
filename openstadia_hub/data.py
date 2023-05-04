from typing import List

from pydantic import parse_obj_as

from .client import Client

clients_dict = [
    {
        'id': '1',
        'token': 'a',
        'title': 'Server 1'
    }
]

clients = parse_obj_as(List[Client], clients_dict)
