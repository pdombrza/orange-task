import requests
import json
import time
from datetime import datetime, timedelta
from typing import Union
import argparse
import sys

from constants import URL, X, Y, FILENAME


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("ex", type=int, default=1, nargs="?")
    arguments = parser.parse_args()
    return arguments


# ex.1
def get_request(path: str) -> requests.models.Response:
    data = requests.get(path)
    return data


# ex.2
def request_time(data: requests.models.Response) -> timedelta:
    return data.elapsed


# ex.3
def get_status_code(data: requests.models.Response) -> int:
    return data.status_code


# ex.4
def get_response_type(data: requests.models.Response) -> Union[str, None]:
    return data.headers.get("Content-Type")


# ex.5
def check_if_req_json_parsable(data: requests.models.Response):
    try:
        json.loads(data.content)
    except json.JSONDecodeError:
        return False
    return True


# ex.6
def log_requests(
    log_period: int, request_amount: int, log_filepath: str, request_url: str
) -> None:
    while True:
        for _ in range(request_amount):
            data = get_request(request_url)
            data_text = data.text.replace("\n", "")
            data_str = f"request time: {datetime.now()}, request_contents: {data_text}, time elapsed: {request_time(data)}, status_code: {get_status_code(data)}, Content-Type: {get_response_type(data)}, is json parsable: {check_if_req_json_parsable(data)}"
            print(data_str)
            write_to_file(log_filepath, data_str)
        time.sleep(log_period)


def write_to_file(filename: str, data: str) -> None:
    with open(filename, "a") as fh:
        fh.write(data + "\n")


def main(args):
    arguments = parse_args(args)
    ex_num = arguments.ex
    data = get_request(URL)
    select_ex = {
        1: get_request,
        2: request_time,
        3: get_status_code,
        4: get_response_type,
        5: check_if_req_json_parsable,
    }
    ex_func = select_ex.get(ex_num)
    if ex_num > 6 or ex_num < 1:
        raise ValueError("Invalid exercise number. Available numbers: 1..6")
    if ex_num == 1:
        return data.text
    if ex_num == 6:
        return log_requests(Y, X, FILENAME, URL)
    return ex_func(data)


if __name__ == "__main__":
    print(main(sys.argv))
