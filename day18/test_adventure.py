import adventure as ad


def test_example():
    input = ad.from_file_data('example.dat')
    _, result = ad.solve_part1(input, 10)
    assert result == 1147
