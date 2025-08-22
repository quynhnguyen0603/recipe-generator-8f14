"""Command-line entry-point:  `python -m katsu_curry ...`"""
import argparse
from .generator import generate_recipe

def main() -> None:
    p = argparse.ArgumentParser(description="Generate a katsu-curry recipe")
    p.add_argument("--protein", default="chicken", choices=["chicken", "pork", "tofu", "shrimp"])
    p.add_argument("--servings", type=int, default=2)
    p.add_argument("--spice", default="medium", choices=["mild", "medium", "hot"])
    p.add_argument("--seed", type=int, help="Random-seed for reproducible garnish selection")
    args = p.parse_args()
    recipe = generate_recipe(args.protein, args.servings, args.spice, args.seed)
    print(recipe)

if __name__ == "__main__":
    main()
