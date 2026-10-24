from core.domain.repository import Repository


class FakeRepository(Repository):
    def __init__(self, initial: list[dict] | None = None) -> None:
        self.filepath = "<memory>"
        self.data: list[dict] = list(initial or [])
        self.save_calls = 0

    def exists(self) -> bool:
        return True

    def load(self) -> list[dict]:
        return list(self.data)

    def save(self, data: list[dict]) -> None:
        self.data = list(data)
        self.save_calls += 1
