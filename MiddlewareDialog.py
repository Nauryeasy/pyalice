from Dialog import Dialog
from typing import Callable


class MiddlewareDialog(Dialog):

    middleware_list = []

    def __init__(self, next_states_list: list, get_response: Callable[[dict], dict], tokens: set):
        super().__init__(next_states_list, get_response, tokens)
        self.middleware_list.append(self)
