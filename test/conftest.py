import pytest

from typing import Any, Callable
from fsm import StateMachine



class DummyStateMachine(StateMachine):
    def __init__(
        self,
        states: Any,
        init_state: Any,
        condition_func: dict[Callable],
        during_func: dict[Callable] = {},
        entry_func: dict[Callable] = {},
        exit_func: dict[Callable] = {},
    ):
        super().__init__(states, init_state, condition_func, during_func, entry_func, exit_func)

    def dummy_transition(self, thresh_step = 2):
        return self.step_counter % thresh_step == 0

    def dummy_action(self):
        pass
    def dummy_condition(self, state_list):
        condition = {state: {} for state in state_list}
        for idx in range(len(state_list) - 1):
            condition[state_list[idx]][state_list[idx + 1]] = self.dummy_transition
        return condition


@pytest.fixture()
def dummy_machine():
    return DummyStateMachine
