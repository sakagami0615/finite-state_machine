from typing import Any, Callable

from fsm.utils import get_function_kwargs


class StateMachine:

    def __init__(
        self,
        states: Any,
        init_state: Any,
        condition_func: dict[Callable],
        during_func: dict[Callable] = {},
        entry_func: dict[Callable] = {},
        exit_func: dict[Callable] = {},
    ):
        self._states = states
        self._init_state = init_state

        self._condition_func = condition_func
        self._during_func = during_func
        self._entry_func = entry_func
        self._exit_func = exit_func

        self._is_self_transition = False

        self._curr_state = None
        self._prev_state = None
        self._next_state = init_state

        self._step_counter = 0

    def _update_state(self) -> None:
        # 自己遷移の処置
        if self._next_state == "self":
            # 自己遷移フラグを立てる
            # 次の状態が自己遷移用の名前になっているため、現在の状態名で置き換える
            self._is_self_transition = True
            self._next_state = self._curr_state
        else:
            self._is_self_transition = False

        # 状態更新
        self._prev_state = self._curr_state
        self._curr_state = self._next_state

    def _change_state(self, **kwargs) -> None:
        # check condition function exist
        if self._curr_state not in self._condition_func:
            return
        for trans_state, condition_func in self._condition_func[
            self._curr_state
        ].items():
            condition_func_kwargs = get_function_kwargs(condition_func, **kwargs)
            if condition_func(**condition_func_kwargs):
                self._next_state = trans_state
                return

    def _is_entry(self) -> bool:
        # check entry function exist
        if self._curr_state not in self._entry_func:
            return False
        # check entry timing
        # 自己繊維フラグが立っている場合もentryを実施する
        return self._prev_state != self._curr_state or self._is_self_transition

    def _is_during(self) -> bool:
        # check during function exist
        if self._curr_state not in self._during_func:
            return False
        return True

    def _is_exit(self) -> bool:
        # check exit function exist
        if self._curr_state not in self._exit_func:
            return False
        # check exit timing
        return self._curr_state != self._next_state

    @property
    def state(self) -> Any:
        return self._curr_state if self._curr_state is not None else self._init_state
    @property
    def next_state(self) -> Any:
        return self._next_state

    @property
    def step_counter(self):
        return self._step_counter

    def step(self, **kwargs) -> Any:
        # update
        self._update_state()
        self._step_counter += 1

        # entry
        if self._is_entry():
            entry_func = self._entry_func[self._curr_state]
            entry_func_kwargs = get_function_kwargs(entry_func, **kwargs)
            entry_func(**entry_func_kwargs)

        # during
        if self._is_during():
            during_func = self._during_func[self._curr_state]
            during_func_kwargs = get_function_kwargs(during_func, **kwargs)
            during_func(**during_func_kwargs)

        # change state
        self._change_state(**kwargs)

        # exit
        if self._is_exit():
            exit_func = self._exit_func[self._curr_state]
            exit_func_kwargs = get_function_kwargs(exit_func, **kwargs)
            exit_func(**exit_func_kwargs)

        return self._curr_state
