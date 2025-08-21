import json
from pep_sphinx_extensions.pep_zero_generator import parser, pep_index_generator

from ..conftest import PEP_ROOT


def test_create_pep_json():
    peps = [parser.PEP(PEP_ROOT / "pep-0008.rst")]

    out = pep_index_generator.create_pep_json(peps)

    data = json.loads(out)
    data = {int(k): v for k, v in data.items()}

    assert 8 in data
    assert data[8]["url"] == "https://peps.python.org/pep-0008/"
