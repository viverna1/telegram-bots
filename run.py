import importlib
import logging
import sys
from pathlib import Path

from core.shared.logger import setup_logging

BOTS_DIR = "src"


def get_bots() -> list[str]:
    src = Path(__file__).parent / BOTS_DIR
    return sorted(p.parent.name for p in src.glob("*/main.py"))


BOTS = get_bots()


def parse_args() -> str:
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    try:
        choice = int(sys.argv[1])
    except ValueError:
        print_usage()
        sys.exit(1)

    if not (1 <= choice <= len(BOTS)):
        print_usage()
        sys.exit(1)

    return f"{BOTS_DIR}.{BOTS[choice - 1]}.main"


def print_usage() -> None:
    print("py run.py <бот>")
    print("\n".join(f"{i + 1}: {bot}" for i, bot in enumerate(BOTS)))


def main():
    module_path = parse_args()
    module = importlib.import_module(module_path)
    module.main()


if __name__ == "__main__":
    setup_logging()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
