import pytest
from katsu_curry import generate_recipe


def test_default_recipe_runs():
    recipe = generate_recipe()  # default params
    assert "Chicken Katsu Curry" in str(recipe)
    assert recipe.servings == 2
    assert recipe.ingredients  # not empty


def test_scaling_quantities():
    two = generate_recipe(servings=2)
    four = generate_recipe(servings=4)
    # Protein should double from 300 g → 600 g
    assert "300 g" in str(two)
    assert "600 g" in str(four)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"protein": "beef"},
        {"servings": 0},
        {"spice_level": "nuclear"},
    ],
)
def test_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        generate_recipe(**kwargs)


def test_deterministic_seed():
    r1 = generate_recipe(seed=42)
    r2 = generate_recipe(seed=42)
    assert r1.ingredients == r2.ingredients
