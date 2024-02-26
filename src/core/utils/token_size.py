import tiktoken
from fastapi import Request

from src.core.utils.strings_constants import constants


def get_token_size(input_str: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")

    encoded_input = encoding.encode(input_str)
    return encoded_input.__len__()


def get_token_from_header(request: Request):
    authorization = request.headers.get(constants.AUTHORIZATION)
    return authorization.split(constants.BEARER_SPACE)[1]
