from git import Repo
import time
from shutil import copy

repo = Repo("/tmp/test")

for commit in list(repo.iter_commits("master", max_count=15)):
    print commit.author, time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commit.committed_date)), commit.message

copy("/tmp/README.md", "/tmp/test/")

repo.index.add(["/tmp/test/README.md"])
repo.index.commit("update from gitpython.")

last_commit = list(repo.iter_commits("master", max_count=15))[1]

git = repo.git
git.reset("--hard", last_commit)
