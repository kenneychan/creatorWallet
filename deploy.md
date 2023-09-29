Set heroku remote repository (do ONCE)

```
heroku git:remote -a creatorwallet
```

Make sure to checkin your features to your feature branch. The following should say "Your branch is up to date with \<your branch>

```
git status
```

Make sure the main branch on your computer is up to date.

Checkout deployment branch

```
git checkout deploy
```

Merge main into deploy branch

```
git fetch
git merge origin/main -m "<comment>"
```

Push heroku deployment branch to remote heroku repository

```
git push heroku deploy:main
```

Note: to deploy from a sub-directory of repository: `git subtree push --prefix <folder> heroku <branch>:main`

Return to feature branch to continue working

```
git checkout <feature branch>
```
