import re
from typing import Dict, List, Set, Tuple

# region testdata
TESTDATA = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
""".splitlines()
# endregion


def parse_foods(data: List[str]) -> Tuple[List[Set[str]], Set[str], Dict[str, List[Set[str]]]]:
    recipes = []
    allergens = {}
    foods = set()
    for line in data:
        m = re.fullmatch(
            r"^((?:[a-z]+ )+)\(contains ((?:[a-z]+(?:, )?)+)\)$", line)
        if m:
            recipe = set(m.group(1).strip().split(" "))
            recipes.append(recipe)
            foods |= recipe
            for allergen in m.group(2).split(", "):
                if allergen not in allergens:
                    allergens[allergen] = []
                allergens[allergen].append(recipe)
    return recipes, foods, allergens


def reduce_allergens(allergens: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
    # every allergen is contained in exactly one food
    # those foods can only be the ones in every combination containing the allergen
    reduced = {}
    for allergen, food_lists in allergens.items():
        foods = set(food_lists[0])
        for food_list in food_lists:
            foods &= set(food_list)
        reduced[allergen] = foods
    return reduced


def part1(data: List[str]):
    recipes, foods, allergens = parse_foods(data)
    reduced = reduce_allergens(allergens)
    allergen_free = foods.difference(*reduced.values())
    # print(foods)
    # print(allergens)
    # print(reduced)
    # print(allergen_free)
    print(sum(1 for recipe in recipes for _ in allergen_free.intersection(recipe)))


if __name__ == "__main__":
    with open("data/21.txt") as f:
        data = f.read()
    data = data.splitlines()
    part1(data)
    # part2(data)
