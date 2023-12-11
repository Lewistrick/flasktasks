import random
from string import ascii_lowercase

from flasktasks.database.task import TaskRecord

def get_random_word():
    return "".join(random.choice(ascii_lowercase) for _ in range(random.randint(2, 10)))

def get_random_sentence():
    return " ".join(get_random_word() for _ in range(random.randint(5, 20)))

def get_random_datestring():
    y = random.randint(2000, 2024)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return f"{y}-{m:02d}-{d:02d}"

def create_fake_task():
    data = {
        "title": get_random_word(),
        "description": get_random_sentence(),
        "due_date": get_random_datestring(),
    }
    print(data)
    TaskRecord(**data).create()

if __name__ == "__main__":
    for _ in range(100):
        create_fake_task()