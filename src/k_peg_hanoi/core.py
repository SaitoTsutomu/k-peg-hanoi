from collections.abc import Iterable
from functools import cache
from importlib.metadata import version
from typing import Annotated

import typer


def main():
    typer.run(show_hanoi)


@cache
def nmove(m: int, n: int) -> int:
    """Minimum number of moves

    :param m: number of disks
    :param n: number of rods
    :return: minimum number of moves
    """
    n = min(m + 1, n)
    if n == 2 and m == 1:
        return 1
    if n <= 2:
        msg = "Too few rods"
        raise ValueError(msg)
    if n == 3:
        return 2**m - 1
    if n == m + 1:
        return 2 * m - 1
    return min(nmove(i, n) * 2 + nmove(m - i, n - 1) for i in range(1, m))


def hanoi(md: int, pos: list[int]) -> Iterable[tuple[int, int]]:
    """Moves of Tower of Hanoi

    :param md: number of disks
    :param pos: position of rods
    :return: from, to
    """
    if md < 1:
        msg = "Too few md"
        raise ValueError(msg)
    if md == 1:
        yield pos[0], pos[-1]
        return
    n = len(pos)
    if n <= 2:
        msg = "Too few len(pos)"
        raise ValueError(msg)
    if n == 3:
        mn = md - 1
    else:
        mn = min((nmove(i, n) * 2 + nmove(md - i, n - 1), i) for i in range(1, md))[1]
    yield from hanoi(mn, [pos[0], *pos[2:], pos[1]])
    yield from hanoi(md - mn, [pos[0], *pos[2:-1], pos[-1]])
    yield from hanoi(mn, [*pos[1:-1], pos[0], pos[-1]])


def _show(towers, count):
    height = max(len(tower) for tower in towers)
    width = max(max(tower, default=0) for tower in towers)
    for i in range(height - 1, -1, -1):
        for tower in towers:
            n = tower[i] if i < len(tower) else 0
            s = "=" * (n * 2 - 1)
            print(f"{s:^{width * 2 - 1}}", end=" ")
        print()
    print(f"{count:-<{width * 2 * len(towers) - 1}}\n")


def _version_callback(*, value: bool):
    if value:
        print(version("k-peg-hanoi"))
        raise typer.Exit


def show_hanoi(
    m: Annotated[int, typer.Argument(min=1, help="Number of disks")],
    n: Annotated[int, typer.Argument(help="Number of rods")] = 3,
    *,
    text: Annotated[bool, typer.Option("--text", help="Show with text")] = False,
    show_version: Annotated[  # ruff: ignore[unused-function-argument]
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = False,
):
    """Show move of Tower of Hanoi"""
    if n < (2 if m == 1 else 3):
        msg = "need at least 3 rods (2 rods only for 1 disk)"
        raise typer.BadParameter(msg, param_hint="n")
    towers = [list(range(m, 0, -1))] + [[] for _ in range(n - 1)]
    if not text:
        _show(towers, 0)
    for i, (fr, to) in enumerate(hanoi(m, list(range(n))), 1):
        towers[to].append(towers[fr].pop())
        if text:
            print(f"#{i} disk {towers[to][-1]} from {fr} to {to}")
        else:
            _show(towers, i)
