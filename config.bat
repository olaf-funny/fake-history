git filter-branch --env-filter '

OLD_EMAIL="alexander.a.alekhin@gmail.com"
CORRECT_NAME="Universal-ops989"
CORRECT_EMAIL="winterhot223@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags


git remote set-url origin git@github.com:Universal-ops989/agTwo.git
git push --force --tags origin 'refs/heads/*'
