from pytest import mark, param
import adventure as ad


@mark.parametrize('input,expect', [
    param('^WNE$', 3),
    param('EWN(E|WWW(NE|N))(WE|N)', 7),
    param('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', 18),
    param('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', 23),
    param('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', 31)
])
def test_solve_part1(input, expect):
    result_site, result_distance = ad.solve_part1(input)
    assert result_distance == expect
