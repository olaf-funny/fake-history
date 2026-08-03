import configparser
import random
from datetime import datetime, timedelta
from pathlib import Path

from git import Repo

# ---- Load config ----
config_path = Path(__file__).parent / "config.ini"
config = configparser.ConfigParser()
if not config.read(config_path):
    raise SystemExit(f"Could not read {config_path}")

s = config["settings"]
REPO_PATH = s.get("repo_path")
START = datetime.strptime(s.get("start_date"), "%Y-%m-%d")
END = datetime.strptime(s.get("end_date"), "%Y-%m-%d")
MAX_PER_DAY = s.getint("max_commits_per_day", fallback=6)
ACTIVE_DAY_CHANCE = s.getfloat("active_day_chance", fallback=0.35)

if START > END:
    raise SystemExit("start_date must be on or before end_date")
if MAX_PER_DAY < 1:
    raise SystemExit("max_commits_per_day must be at least 1")

LOG_PATH = f"{REPO_PATH}/log.txt"

# Counts 1..MAX_PER_DAY, with higher counts getting progressively rarer
counts = list(range(1, MAX_PER_DAY + 1))
weights = [1 / (n ** 1.5) for n in counts]

repo = Repo(REPO_PATH)
total = 0

days = (END - START).days + 1
for offset in range(days):
    current = START + timedelta(days=offset)

    # Skip weekends (Saturday=5, Sunday=6)
    if current.weekday() >= 5:
        continue

    # Most weekdays have no commits
    if random.random() > ACTIVE_DAY_CHANCE:
        continue

    num_commits = random.choices(counts, weights=weights, k=1)[0]
    minutes = sorted(random.sample(range(9 * 60, 21 * 60), num_commits))

    for m in minutes:
        when = current + timedelta(minutes=m)
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S")

        with open(LOG_PATH, "a") as f:
            f.write(f"Entry for {stamp}\n")

        repo.git.add(A=True)
        repo.index.commit(f"Update {stamp}", author_date=stamp, commit_date=stamp)
        total += 1

print(f"Created {total} commits between {START:%Y-%m-%d} and {END:%Y-%m-%d}")

repo.remote("origin").push()
print("Pushed to origin")