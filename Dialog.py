from typing import Callable


class Dialog:
    def __init__(self, next_states_list: list, get_response: Callable[[dict], dict], tokens: set, last_state=None, always=False):
        self.next_states_list = next_states_list
        self.get_response = get_response
        self.last_state = last_state
        self.tokens = tokens
        self.always = always

    def get_response_info(self, event:dict) -> dict:
        return self.get_response(event)

    def set_last_state(self, last_state: object) -> None:
        self.last_state = last_state

    def set_next_states_list(self, next_states_list: list) -> None:
        self.next_states_list = next_states_list

    def set_always(self, always: bool) -> None:
        self.always = always
