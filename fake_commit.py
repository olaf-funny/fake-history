import git

git_repo = git.Repo("D:\\workspace\\fake-history", search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")
print("------------------------")
if __name__ == "__main__":
    print(git_root)
print("------------------------")

## B. START: Git process
# Auto from search (A) above
repo = git.Repo(git_root)
# Or manual enter repo path, note in this case, Windows is forward slash (X:/)
#repo = git.Repo('X:/devops-roadmap-master')

## B1. Checkout
origin = repo.remote(name='origin')
# Note:  Branch is usually 'main' but can be 'master'
branch_name = repo.active_branch.name
print(f"Using branch: {branch_name}")

## B2. Do some changes and Add -> Commit
repo.git.add(all=True)
print('Files Added Successfully')
repo.index.commit('Delete bat file')
print('Committed successfully')

## B3. Push to the repo
origin.push()
print('Pushed changes to origin')