from enum import Enum

from fsm import StateMachine


class SampleStateMachine(StateMachine):

    class State(Enum):
        A = 1
        B = 2

    def __init__(self):
        self._setting()
        super().__init__(self._states, self._init_state, self._condition_func, self._during_func, self._entry_func, self._exit_func)
        self._count = 0
        self._value = 0

    def _setting(self):
        # 状態
        self._states = list(self.State)
        self._init_state = self.State.A

        # 遷移条件
        self._condition_func = {
            self.State.A: {
                self.State.B: self._a_to_b_condition,
            },
            self.State.B: {
                self.State.A: self._b_to_a_condition,
            },
        }

        # 各状態での実施処理
        self._during_func = {
            self.State.A: self._a_during,
            self.State.B: self._b_during
        }
        self._entry_func = {
            self.State.A: self._a_entry,
            self.State.B: self._b_entry
        }
        self._exit_func = {
            self.State.A: self._a_exit,
            self.State.B: self._b_exit
        }

    def _a_to_b_condition(self, thresh_count):
        return self._count % thresh_count == 0

    def _b_to_a_condition(self, thresh_count):
        return self._count % thresh_count == 0

    def _a_entry(self):
        print("<a_entry>")
        self._count = 0

    def _b_entry(self):
        print("<b_entry>")
        self._count = 0

    def _a_during(self, add_score):
        print("<a_during>")
        self._count += 1
        self._value += add_score

    def _b_during(self, add_score):
        print("<b_during>")
        self._count += 1
        self._value += add_score

    def _a_exit(self):
        print("<a_exit>")
        self._count = 0

    def _b_exit(self):
        print("<b_exit>")
        self._count = 0

    @property
    def value(self):
        return self._value


if __name__ == "__main__":

    machine = SampleStateMachine()

    def one_step():
        curr_state = machine.step(add_score=10, thresh_count=3)
        print(f"{curr_state} -> {machine._next_state}")
        print(f"(count, value) = ({machine._count}, {machine._value})")
        print("-" * 20)

    one_step()
    one_step()
    one_step()
    one_step()
    one_step()
    one_step()
    one_step()
