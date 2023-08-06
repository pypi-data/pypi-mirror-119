from typing import List, Tuple


class BlauMove:
    factory_idx: int
    color: int
    working_row: int

    def __init__(self, factory_idx: int, cidx: int, working_row: int):
        ...


class BlauState:
    curr_player_idx: int = ...

    def __init__(self, names: List[str]):
        ...

    def do_move(self, m: BlauMove) -> bool:
        ...

    def finish_round(self) -> bool:
        ...

    def start_round(self) -> None:
        ...

    def to_json(self) -> str:
        ...

    def players(self) -> List[Tuple[str, int]]:
        ...

    def is_finished(self) -> bool:
        ...


class BlauAgent:
    def __init__(self, level: int):
        ...

    def choose_action(self, game: BlauState) -> BlauMove:
        ...
