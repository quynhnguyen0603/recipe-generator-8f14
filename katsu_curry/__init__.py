"""
Katsu-curry recipe generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import::

    from katsu_curry import generate_recipe
    print(generate_recipe())          # default chicken, 2 servings, medium
    print(generate_recipe("pork", 4)) # pork katsu for 4

Run as module::

    python -m katsu_curry --protein tofu --servings 1 --spice mild
"""
from .generator import generate_recipe, KatsuCurryRecipe  # re‑export
__all__ = ["generate_recipe", "KatsuCurryRecipe"]
