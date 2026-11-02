import random
from datetime import datetime, timedelta
from git import Repo

REPO_PATH = "D:/workspace/fake-history"
LOG_PATH = f"{REPO_PATH}/log.txt"

repo = Repo(REPO_PATH)

start = datetime.now() - timedelta(days=10)
total = 0

for day in range(365):
    current = start + timedelta(days=day)

    # weekday(): Monday=0 ... Saturday=5, Sunday=6
    if current.weekday() >= 5:
        continue

    num_commits = random.randint(0, 6)
    if num_commits == 0:
        continue

    # Random, sorted times within the day so commits stay in chronological order
    minutes_in_day = sorted(random.sample(range(9 * 60, 21 * 60), num_commits))

    for m in minutes_in_day:
        when = current.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=m)
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S")

        with open(LOG_PATH, "a") as f:
            f.write(f"Entry for {stamp}\n")

        repo.git.add(A=True)
        repo.index.commit(
            f"Update {stamp}",
            author_date=stamp,
            commit_date=stamp,
        )
        total += 1

print(f"Created {total} commits")

# Push once at the end
repo.remote("origin").push()
print("Pushed to origin")