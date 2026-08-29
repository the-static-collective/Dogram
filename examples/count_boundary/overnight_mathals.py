import json

from dogram.count_boundary import walk_registry


REGISTRY = {
    (12, 13),
    (17, 18),
    (81, 82),
    (107, 108),
    (136, 137),
    (180, 181),
    (207, 208),
    (1007, 1008),
    (1078, 1087),
    (1107, 1108),
}


if __name__ == "__main__":
    result = walk_registry((1078, 1087), REGISTRY, max_depth=4)
    print(json.dumps(result, indent=2, sort_keys=True))
