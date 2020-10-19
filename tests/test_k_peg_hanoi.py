from k_peg_hanoi import hanoi


def test_moves(snapshot):
    cases = [
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
    ]
    for m, n, e in cases:
        result = list(hanoi(m, list(range(n))))
        assert len(result) == e
        snapshot.assert_match(result)
