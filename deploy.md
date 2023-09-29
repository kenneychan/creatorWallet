# Pre-setup

Create Heroku app

```
heroku create creatorwallet2
```

Set heroku remote repository (do ONCE)

```
heroku git:remote -a creatorwallet
```

Set environment variables

```
heroku config:set AWS_SECRET_ACCESS_KEY=<key>
heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set S3_BASE_URL=<url>
heroku config:set S3_BUCKET=<bucket>
heroku config:set TWITCH_APP_TOKEN=<token>
heroku config:set TWITCH_CLIENT_ID=<id>
heroku config:set YOUTUBE_API_KEY=<key>
heroku config:set DATABASE_URL=<url>
```

# Deploy updates

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
git checkout deploy-neon
```

Merge main into deployment branch

```
git fetch
git merge origin/main -m "<comment>"
```

Push heroku deployment branch to remote heroku repository
Note: to deploy from a sub-directory of repository: `git subtree push --prefix=<folder> heroku <branch>:main`

```
git subtree push --prefix=creatorwallet/ heroku deploy-neon:main
```

Return to feature branch to continue working

```
git checkout <feature branch>
```
