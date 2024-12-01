import pytest



@pytest.mark.parametrize(["is_entry", "is_during", "is_exit", "is_condition_list", "expected_list"], [
    pytest.param(True, False, False, [True, False], ["en", "en"], id="(entry) init condition true"),
    pytest.param(True, False, False, [False, True], ["en"], id="(entry) second condition true"),
    pytest.param(False, False, True, [True, False], ["ex"], id="(exit) init condition true"),
    pytest.param(False, False, True, [False, False], [], id="(exit) not condition true"),
    pytest.param(False, True, False, [False, False, False], ["du", "du", "du"], id="(during) not condition true"),
    pytest.param(True, True, True, [True], ["en", "du", "ex"], id="(entry, during, exit) init condition true"),
    pytest.param(True, True, True, [False, True], ["en", "du", "du", "ex"], id="(entry, during, exit) second condition true"),
])
def test_sm_action(dummy_machine, is_entry, is_during, is_exit, is_condition_list, expected_list):

    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A"], "A", {"A": {"self": self.condition}}, {"A": self.during_action}, {"A": self.entry_action}, {"A": self.end_action})
            self.action_values = []

        def condition(self, x = False): return x
        def entry_action(self):
            if is_entry: self.action_values.append("en")
        def during_action(self):
            if is_during: self.action_values.append("du")
        def end_action(self):
            if is_exit: self.action_values.append("ex")

    machine = TestMachine()
    for x in is_condition_list:
        machine.step(x = x)
    assert machine.action_values == expected_list
