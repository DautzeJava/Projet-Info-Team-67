import json  # to read the JSON file

RESOURCES = ["gold", "mana", "diamonds"]  # the only allowed resource names
COMMON = ["id", "name", "symbol", "type", "zone", "price", "production",
          "consumption", "max_count", "max_level", "requires", "hp"]  # keys every building needs
EXTRA = {"defense": ["damage", "range"], "trap": ["damage"]}  # keys needed by some types

with open("data/buildings.json", "r", encoding="utf-8") as f:  # open the file
    buildings = json.load(f)["buildings"]  # get the list of buildings

errors = []  # we collect every problem here
ids = []  # we collect the ids to detect duplicates

for b in buildings:  # check each building
    name = b.get("id", "???")  # id used in error messages
    ids.append(name)
    needed = COMMON + EXTRA.get(b.get("type"), [])  # keys required for this type
    for key in needed:
        if key not in b:
            errors.append(name + ": missing key '" + key + "'")
    for field in ["production", "consumption"]:  # check resource names
        for res in b.get(field, {}):
            if res not in RESOURCES:
                errors.append(name + ": unknown resource '" + res + "' in " + field)

for i in ids:  # duplicate ids
    if ids.count(i) > 1:
        errors.append("duplicate id: " + i)

if errors:
    print("PROBLEMS:")
    for e in errors:
        print(" -", e)
else:
    print("OK:", len(buildings), "buildings")