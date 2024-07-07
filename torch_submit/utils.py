import random


def generate_friendly_name():
    adjectives = [
        "happy",
        "sunny",
        "clever",
        "swift",
        "brave",
        "bright",
        "calm",
        "daring",
        "eager",
        "gentle",
        "jolly",
        "kind",
        "lively",
        "nice",
        "proud",
        "wise",
    ]
    nouns = [
        "panda",
        "tiger",
        "eagle",
        "dolphin",
        "fox",
        "owl",
        "wolf",
        "bear",
        "hawk",
        "lion",
        "deer",
        "rabbit",
        "otter",
        "koala",
        "lynx",
        "raven",
    ]
    return f"{random.choice(adjectives)}-{random.choice(nouns)}"
