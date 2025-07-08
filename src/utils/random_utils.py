import random
from typing import Optional

def get_random_generator(seed: Optional[int] = None) -> random.Random:
    return random.Random(seed)