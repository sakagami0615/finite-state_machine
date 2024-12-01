import pytest


def test_sm_default_argument_entry(dummy_machine):
    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A"], "A", {"A": {"self": self.callback_condition}}, {}, {"A": self.callback_action}, {})
            self.y = 0
        def callback_condition(self): return True
        def callback_action(self, y = 1): self.y = y

    machine = TestMachine()
    assert machine.y == 0
    machine.step()
    assert machine.y == 1
    machine.step(y = 2)
    assert machine.y == 2


def test_sm_default_argument_during(dummy_machine):
    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A"], "A", {}, {"A": self.callback_action}, {}, {})
            self.y = 0
        def callback_action(self, y = 1): self.y = y

    machine = TestMachine()
    assert machine.y == 0
    machine.step()
    assert machine.y == 1
    machine.step(y = 2)
    assert machine.y == 2


def test_sm_default_argument_exit(dummy_machine):
    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A"], "A", {"A": {"self": self.callback_condition}}, {}, {}, {"A": self.callback_action})
            self.y = 0

        def callback_condition(self, x = 0): return x == 1
        def callback_action(self, y = 1): self.y = y

    machine = TestMachine()
    assert machine.y == 0
    machine.step()
    assert machine.y == 0
    machine.step(x = 1)
    assert machine.y == 1
    machine.step(x = 1, y = 2)
    assert machine.y == 2
