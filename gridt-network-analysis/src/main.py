from network_analysis import plot_network

import sys
import requests

DEFAULT_MOVEMENT_ID = 1
EMAIL = 'admin@gridt.org'
PASSWORD = 'insecure'
BASE_URL = 'https://api.gridt.org'


def main(movement_id: int = DEFAULT_MOVEMENT_ID) -> None:
    print(f"Lets do some network analysis on movement {movement_id}.")
    token = login()
    edges, nodes = get_movement_data(movement_id, token)
    plot_network(nodes=nodes, edges=edges)


def login() -> str:
    print("Logging in...", end='\t')
    token = get_token()
    if token is None:
        print("could not login.")
        exit(1)
    print("done.")
    return token


def get_token() -> str:
    url = f'{BASE_URL}/auth'
    body = dict(username=EMAIL, password=PASSWORD)
    response = requests.post(url=url, json=body)
    return response.json()['access_token']


def get_movement_data(id: int, token: str) -> tuple:
    print("Loading data...", end='\t')
    url = f'{BASE_URL}/movements/{id}/data'
    header = dict(authorization=f'JWT {token}')
    response = requests.get(url=url, headers=header)
    response_json = response.json()
    print("done.")
    return response_json.get('edges', []), response_json.get('nodes', [])


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        main()
    elif argc == 2:
        main(sys.argv[1])
    else:
        print(f"Unexpected additional parameters: {sys.argv[2:]}")
        print(f"Usage:\npython {sys.argv[0]} <movement_id>")
