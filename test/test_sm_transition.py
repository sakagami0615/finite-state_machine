import pytest



def test_sm_self_transition(dummy_machine):

    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A"], "A", {"A": {"self": self.dummy_transition}},
                             {"A": self.dummy_action}, {"A": self.entry_action}, {"A": self.dummy_action})
            self.entry_count = 0
        def entry_action(self):
            self.entry_count += 1

    machine = TestMachine()
    machine.step(thresh_step=2)
    machine.step(thresh_step=2)
    machine.step(thresh_step=2)
    assert machine.entry_count == 2


def test_sm_transition_priority(dummy_machine):

    class TestMachine(dummy_machine):
        def __init__(self):
            super().__init__(["A", "B", "C"], "A", {"A": {"C": self.dummy_transition, "B": self.dummy_transition}})

    machine = TestMachine()
    machine.step(thresh_step=1)
    machine.step(thresh_step=2)
    assert machine.state == "C"
