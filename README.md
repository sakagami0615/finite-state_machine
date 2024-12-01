# finite-state-machine

pythonで状態遷移を使用するために作成したものです。

## 状態遷移クラス(StateMachine)

入力情報は下記の通り

`states` datatype: *Any*  
状態変数リスト  

`init_state` datatype: *Any*  
初期状態  

`condition_func` datatype: *dict[Callable]* (default: {})  
各状態への遷移条件  

```python
{"A": 
    # 状態"A"から状態"B"への遷移
    "B": <callback function (return True or False)>,
    # 自己遷移
    "self": <callback function (return True or False)>,
}
```

`during_func` datatype: *dict[Callable]* (default: {})  
各状態の時に実施する処理  

```python
{"A": <callback function (return True or False)>,
 "B": <callback function (return True or False)>}
```

`entry_func` datatype: *dict[Callable]* (default: {})  
状態の最初に実施する処理  

```python
{"A": <callback function (return True or False)>,
 "B": <callback function (return True or False)>}
```

`exit_func` datatype: *dict[Callable]* (default: {})  
状態の最後に実施する処理  

```python
{"A": <callback function (return True or False)>,
 "B": <callback function (return True or False)>}
```

## 使い方

下記のクラスを import し、このクラスを継承したオリジナルの状態遷移クラスを定義するようになっています。

```python
from fsm import StateMachine
```

### 状態遷移のクラスを準備

StateMachine クラスを継承し、クラス内で下記内容を定義します。

- `state list` 状態変数
- `init state` 遷移条件
- `during action` 各状態の時に実施する処理
- `entry action`, `exit_action` 状態が切り替わるときに実施する処理

#### 基本的な使い方

```python
class MyStateMachine(StateMachine):

    def __init__(self, ["A", "B"],          # state list
                       "A",                 # init state
                       {
                            "A": {
                                "B": self.sample_condition,         # a to b transition condition
                                "self": self.sample_self_condition, # self transition condition
                            },
                            "B": {
                                "A": self.sample_condition,         # b to a transition condition
                                "self": self.sample_self_condition, # self transition condition
                            }
                       },
                       {
                            "A": self.sample_entry_action,          # a entry action callback
                            "B": self.sample_entry_action,          # b entry action callback
                       },
                       {
                            "A": self.sample_during_action,         # a during action callback
                            "B": self.sample_during_action,         # b during action callback
                       },
                       {
                            "A": self.sample_exit_action,           # a exit action callback
                            "B": self.sample_exit_action,           # b exit action callback
                       }
                ):

    # 各内容の処理をメンバ関数で用意
    def sample_condition() -> bool:
        # <your logic here>
    def sample_self_condition() -> None:
        # <your logic here>
    def sample_entry_action() -> None:
        # <your logic here>
    def sample_during_action() -> None:
        # <your logic here>
    def sample_exit_action() -> None:
        # <your logic here>
```

#### Enum状態変数を使用する場合

```python
class MyState(Enum):
    A = 1
    B = 2

class MyStateMachine(StateMachine):
    def __init__(self, list(MyState),
                       MyState.A,
                       {
                            MyState.A,: {
                                MyState.B: <callback function>
                                "self": <callback function>
                            },
                       ...
                       },
                )
```

#### メンバ変数を追加し、状態遷移条件に使用する場合

```python
class MyStateMachine(StateMachine):

    def __init__(self, ["A", "B"], "A",
                       {"A": {"B": self.sample_condition}},
                ):
        self._value = 0

    def sample_condition() -> bool:
        if self._value >= 3:
            return True
        self._value += 1
        return False
```

#### コールバック関数に引数を追加する場合

```python
class MyStateMachine(StateMachine):

    # ここの記載は変化なし
    def __init__(self, ["A", "B"], "A",
                       {"A": {"B": self.sample_condition}},
                       {"A": self.sample_entry_action},
                       {"A": self.sample_during_action},
                       {"A": self.sample_exit_action}
                ):

    # 下記のメンバ変数に引数を追加できる。
    # 追加した場合は、「用意したクラスを使用する」の step 関数実施時に
    # キーワード引数として追加する必要がある。
    def sample_condition(arg1) -> bool:
        pass
    # メンバ間で引数を統一する必要はない
    def sample_self_condition(arg1, arg2) -> None:
        pass
    def sample_entry_action(arg3) -> None:
        pass
    # 引数指定しないメンバ関数があってもよい
    def sample_during_action() -> None:
        pass
    # デフォルト引数も設定可能
    def sample_exit_action(arg4 = 3) -> None:
```

### 用意したクラスを使用する

#### 基本的な使い方

```python
machine = MyStateMachine()

machine.step()      # 処理実行

print(machine.step)             # step実行時の状態を表示
print(machine.step_counter)    # step実行数を表示
```

#### 引数指定をする場合

「コールバック関数に引数を追加する場合」で作成したクラスを使用する場合

```python
machine = MyStateMachine()

# arg4 はデフォルト引数を設定しているため、なくても問題ない
machine.step(arg1 = 1, arg2 = 2, arg3 = 3)

print(machine.step)             # step実行時の状態を表示
print(machine.step_counter)    # step実行数を表示
```