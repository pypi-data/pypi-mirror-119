# type: ignore

import pytest
from modelbase.ode import Model


def test_generate_compounds_source_code_single():
    model = Model()
    model.add_compound("x")
    expected = "m.add_compounds(compounds=['x'])"
    assert expected == model._generate_compounds_source_code(include_meta_info=False)
    expected = "m.add_compounds(compounds=['x'], meta_info={'x': {'compartment': 'c'}})"
    assert expected == model._generate_compounds_source_code(include_meta_info=True)


def test_generate_compounds_source_code_multiple():
    model = Model()
    model.add_compounds(["x", "y"])
    expected = "m.add_compounds(compounds=['x', 'y'])"
    assert expected == model._generate_compounds_source_code(include_meta_info=False)
    expected = "m.add_compounds(compounds=['x', 'y'], meta_info={'x': {'compartment': 'c'}, 'y': {'compartment': 'c'}})"
    assert expected == model._generate_compounds_source_code(include_meta_info=True)
