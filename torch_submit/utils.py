import json
import random
from typing import Dict, Optional


def generate_friendly_name() -> str:
    """Generate a friendly, human-readable name for a job.

    This function creates a name by combining a random adjective, a random animal noun,
    and a random 4-digit number. The name format is 'adjective-noun-number'.

    Returns:
        A friendly name string in the format 'adjective-noun-number'.

    Example:
        >>> generate_friendly_name()
        'happy-panda-3721'
    """
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
    return f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(1000, 9999)}"


def get_job_metadata() -> Optional[Dict[str, str]]:
    """Retrieve job metadata from the '.torch/job.json' file.

    This function attempts to read and parse the job metadata stored in the
    '.torch/job.json' file in the current working directory.

    Returns:
        A dictionary containing job metadata if the file exists and can be parsed
        successfully, or None if the file is not found.

    Raises:
        json.JSONDecodeError: If the file exists but contains invalid JSON.

    Example:
        >>> metadata = get_job_metadata()
        >>> if metadata:
        ...     print(f"Job ID: {metadata.get('id')}")
        ... else:
        ...     print("No job metadata found.")
    """
    try:
        with open(".torch_submit/job.json", "r") as f:
            job_metadata = json.load(f)
            return job_metadata
    except FileNotFoundError:
        return None
