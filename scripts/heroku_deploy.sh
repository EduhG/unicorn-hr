#!/bin/bash

APP_NAME=$1

if ! git remote | grep -q heroku; then
    git remote add heroku git@heroku.com:$APP_NAME.git
fi

git fetch heroku

MIGRATION_CHANGES=$(git diff HEAD heroku/master --name-only -- migrations app/models.py | wc -l)
DATABASE_TABLES=$(heroku pg:info -a $APP_NAME | grep Tables | awk -F':' '{print $2}' | tr -d ' ')

echo "$MIGRATION_CHANGES db changes."

PREV_WORKERS=$(heroku ps --app $APP_NAME | grep "^worker." | wc -l | tr -d ' ')

# migrations require downtime so enter maintenance mode
if test $MIGRATION_CHANGES -gt 0; then
    heroku maintenance:on --app $APP_NAME

    # Make sure workers are not running during a migration
    heroku scale worker=0 --app $APP_NAME
fi

# create db in heroku if used by app
if [ "$CREATE_DB" = "1" ] && ! heroku config | grep -q DATABASE_URL; then
    heroku addons:create heroku-postgresql:hobby-dev
fi

# deploy code changes (and implicitly restart the app and any running workers)
git push heroku $CIRCLE_SHA1:refs/heads/master

# run database migrations if needed and restart background workers once finished
if test $MIGRATION_CHANGES -gt 0; then
    if [ "$CREATE_DB" = "1" ] && [[ "$DATABASE_TABLES" = 0 ]]; then
        heroku run python manage.py init_app
    elif [ "$CREATE_DB" = "1" ]; then
        heroku run python manage.py db upgrade
    fi
    heroku scale worker=$PREV_WORKERS --app $APP_NAME
    heroku restart --app $APP_NAME
fi

heroku maintenance:off --app $APP_NAME
