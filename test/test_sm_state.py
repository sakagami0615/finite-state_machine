import pytest

from enum import Enum


class DummyState(Enum):
    A = 1
    B = 2
    C = 3



@pytest.mark.parametrize(["state_list"], [
    pytest.param(["A", "B", "C"], id="string"),
    pytest.param([1, 2, 3], id="integer"),
    pytest.param(list(DummyState), id="enum"),
])
def test_sm_state_datatype(dummy_machine, state_list):
    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(state_list, state_list[0], self.dummy_condition(state_list))

    machine = TestMachine()
    for s in state_list:
        machine.step(thresh_step=1)
        assert machine.state == s


@pytest.mark.parametrize(["state_list"], [
    pytest.param(["A", "B", "C"], id="string"),
    pytest.param([1, 2, 3], id="integer"),
    pytest.param(list(DummyState), id="enum"),
])
def test_sm_next_state(dummy_machine, state_list):
    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(state_list, state_list[0], self.dummy_condition(state_list))

    machine = TestMachine()
    next_state_list = state_list[1:] + [state_list[-1]]
    for s in next_state_list:
        machine.step(thresh_step=1)
        assert machine.next_state == s
