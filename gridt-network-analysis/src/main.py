from network_analysis import plot_network

import sys
import subprocess
import json

DEFAULT_MOVEMENT_ID = 1
EMAIL = 'admin@gridt.org'
PASSWORD = 'insecure'


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
    cmd = (
        "curl -k --silent --location 'https://localhost/auth' "
        "--header 'HOST: api.gridt.org' "
        "--header 'Content-Type: application/json' "
        "--data-raw '{"
        f"\"username\": \"{EMAIL}\", "
        f"\"password\": \"{PASSWORD}\""
        "}'; exit 0"
    )
    returned_output = subprocess.check_output(cmd, shell=True)
    response = json.loads(returned_output.decode('utf-8'))
    return response.get('access_token')


def get_movement_data(id: int, token: str) -> tuple:
    print("Loading data...", end='\t')
    cmd = (
        f"curl -k --silent --location 'https://localhost/movements/{id}/data' "
        "--header 'Host: api.gridt.org' "
        f"--header 'Authorization: JWT {token}'; exit 0"
    )
    returned_output = subprocess.check_output(cmd, shell=True)
    response = json.loads(returned_output.decode('utf-8'))
    print("done.")
    return response.get('edges', []), response.get('nodes', [])


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1:
        main()
    elif argc == 2:
        main(sys.argv[1])
    else:
        print(f"Unexpected additional parameters: {sys.argv[2:]}")
        print(f"Usage:\npython {sys.argv[0]} <movement_id>")
