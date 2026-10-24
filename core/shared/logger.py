# logger.py
import logging


class ExcludeLoggersFilter(logging.Filter):
    """Пропускает всё, кроме логгеров из списка (по префиксу)."""

    def __init__(self, excluded: tuple[str, ...]):
        super().__init__()
        self.excluded = excluded

    def filter(self, record: logging.LogRecord) -> bool:
        return not record.name.startswith(self.excluded)


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(name)s: %(message)s"
    ))
    handler.addFilter(ExcludeLoggersFilter((
        # "aiogram",   # раскомментируйте, если нужно спрятать и aiogram
        "aiogram.event",
        "aiohttp",
        "asyncio",
    )))

    # basicConfig сам прицепит handler к root-логгеру.
    # force=True — чтобы при повторном вызове не было дублей.
    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )