from __future__ import annotations

import random
from dataclasses import dataclass, field
from textwrap import dedent

_PROTEINS = {
    "chicken": "skinless chicken breast",
    "pork": "pork loin cutlet",
    "tofu": "extra-firm tofu",
    "shrimp": "jumbo shrimp (peeled, deveined)",
}

_SPICE_MAP = {
    "mild": 0.6,
    "medium": 1.0,
    "hot": 1.4,
}


@dataclass
class KatsuCurryRecipe:
    """A fully rendered katsu-curry recipe."""
    title: str
    servings: int
    ingredients: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)

    def __str__(self) -> str:  # pretty-print
        ing = "\n".join(f"• {i}" for i in self.ingredients)
        stp = "\n".join(f"{idx}. {s}" for idx, s in enumerate(self.steps, 1))
        return dedent(
            f"""
            {self.title}
            {'=' * len(self.title)}

            Servings: {self.servings}

            Ingredients
            -----------
            {ing}

            Method
            ------
            {stp}
            """
        ).strip()


def _scale(qty: float, factor: float, unit: str) -> str:
    """Return human-readable quantity rounded to 1 decimal if needed."""
    value = round(qty * factor, 1)
    # Beautify integers like 2.0 → 2
    value = int(value) if value.is_integer() else value
    return f"{value} {unit}"


def generate_recipe(
    protein: str = "chicken",
    servings: int = 2,
    spice_level: str = "medium",
    seed: int | None = None,
) -> KatsuCurryRecipe:
    """
    Produce a deterministic or randomized katsu-curry recipe.

    Parameters
    ----------
    protein : chicken | pork | tofu | shrimp
    servings : positive int
    spice_level : mild | medium | hot
    seed : int, for reproducible random veggie garnish selection
    """
    if protein not in _PROTEINS:
        raise ValueError(f"Unsupported protein '{protein}'. Choose from {list(_PROTEINS)}")
    if servings < 1:
        raise ValueError("servings must be >= 1")
    if spice_level not in _SPICE_MAP:
        raise ValueError(f"spice_level must be one of {list(_SPICE_MAP)}")

    rng = random.Random(seed)

    # --- Ingredient math --------------------------------------------------
    factor = servings
    spice_factor = _SPICE_MAP[spice_level]

    # Base weights / volumes per serving
    per = {
        "protein_g": 150,
        "onion_g": 75,
        "carrot_g": 60,
        "garlic_clove": 0.5,
        "ginger_g": 5,
        "curry_powder_tsp": 1 * spice_factor,
        "flour_sauce_tbsp": 1,
        "honey_tsp": 1,
        "soy_sauce_tsp": 1,
        "stock_ml": 150,
        "rice_g": 75,
    }

    veg_garnishes = ["shredded cabbage", "sliced radish", "pickled ginger"]
    # Randomly decide whether to add cucumber or edamame
    if rng.random() < 0.5:
        veg_garnishes.append("thin-sliced cucumber")
    if rng.random() < 0.5:
        veg_garnishes.append("steamed edamame")

    # --- Ingredient list --------------------------------------------------
    ingredients = [
        f"{_scale(per['protein_g'], factor, 'g')} {_PROTEINS[protein]}",
        f"{_scale(per['flour_sauce_tbsp'], factor, 'Tbsp')} plain flour (for sauce)",
        f"{_scale(1, factor, 'egg')}  (for breading)",
        f"{_scale(50, factor, 'g')} panko breadcrumbs",
        f"{_scale(30, factor, 'ml')} neutral frying oil",
        # Sauce veg
        f"{_scale(per['onion_g'], factor, 'g')} onion, finely diced",
        f"{_scale(per['carrot_g'], factor, 'g')} carrot, diced",
        f"{_scale(per['garlic_clove'], factor, 'clove')} garlic, minced",
        f"{_scale(per['ginger_g'], factor, 'g')} fresh ginger, minced",
        f"{_scale(per['curry_powder_tsp'], factor, 'tsp')} Japanese curry powder",
        f"{_scale(per['flour_sauce_tbsp'], factor, 'Tbsp')} plain flour (to thicken sauce)",
        f"{_scale(per['honey_tsp'], factor, 'tsp')} honey",
        f"{_scale(per['soy_sauce_tsp'], factor, 'tsp')} soy sauce",
        f"{_scale(per['stock_ml'], factor, 'ml')} chicken or vegetable stock",
        f"{_scale(per['rice_g'], factor, 'g')} short-grain Japanese rice, cooked",
        # Garnish
        *(veg_garnishes),
    ]

    # --- Method steps -----------------------------------------------------
    steps = [
        "Prepare rice according to package instructions so it is ready when the curry is done.",
        f"Season the {_PROTEINS[protein]} with salt and pepper. Dredge in flour, dip in beaten egg, then coat with panko.",
        "Heat oil in a skillet to 170 °C (340 °F). Fry cutlets until golden and cooked through (about 3-4 min per side). Rest on a rack.",
        "Sauce: In a saucepan sauté onion, carrot, garlic and ginger until softened.",
        "Add curry powder; cook 30 s. Sprinkle flour, stir 1 min.",
        "Whisk in stock gradually until smooth. Add honey and soy. Simmer 10 min until thick. Blend if you prefer a smoother sauce.",
        "Slice katsu cutlets. Plate rice, ladle curry sauce, place sliced katsu on top.",
        "Garnish with shredded cabbage or other chosen veggies. Serve immediately.",
    ]

    title = f"{protein.capitalize()} Katsu Curry ({spice_level})"

    return KatsuCurryRecipe(title=title, servings=servings, ingredients=ingredients, steps=steps)
