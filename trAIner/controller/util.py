from string import ascii_letters
from random import choice, sample
from faker import Faker
from faker.providers import internet
from config import config

def get_fake():
    fake = Faker('ko_KR')
    fake.add_provider(internet)
    return fake


def snake2pascal(string: str):
    """String Convert: snake_case to PascalCase"""
    return (
        string
        .replace("_", " ")
        .title()
        .replace(" ", "")
    )


def pascal2snake(string: str):
    """String Convert: PascalCase to snake_case"""
    return ''.join(
        word.title() for word in string.split('_')
    )


def get_random_id():
    """Get Random String for Identification"""
    string_pool = ascii_letters + "0123456789"
    rand_string = [choice(string_pool) for _ in range(15)]
    return "".join(rand_string)


def get_random_index(
    length: int = 50,
    count: int = 10
):
    """Get random index"""
    return sample(range(length), count)


def get_tier(tier: str):
    if tier == 'bronze':
        return [1,2,3,4,5]
    elif tier == 'silver':
        return [6,7,8,9,10]
    elif tier == 'gold':
        return [11,12,13,14,15]
    else:
        return RuntimeError('Invalid Tier')


def make_tier_map():
    tiers = config.AVAILABLE_TIER
    result = {}
    for i in tiers:
        result[i] = None
    return tiers, result

if __name__ == '__main__':
    print(get_random_index(count=1))