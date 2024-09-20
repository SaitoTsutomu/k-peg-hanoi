import pytest

from k_peg_hanoi import hanoi


@pytest.mark.parametrize(
    ("md", "size", "n_hands"),
    [
        (1, 2, 1),
        (2, 3, 3),
        (2, 4, 3),
        (3, 3, 7),
        (3, 4, 5),
        (4, 3, 15),
        (4, 4, 9),
        (4, 5, 7),
        (6, 4, 17),
        (8, 3, 255),
    ],
)
def test_moves(snapshot, md, size, n_hands):
    result = list(hanoi(md, list(range(size))))
    assert len(result) == n_hands
    snapshot.assert_match(str(result), "result.txt")
