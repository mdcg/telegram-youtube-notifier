#!/bin/bash
heroku login
heroku git:remote -a yt-shevchenko
heroku stack:set container
git push heroku main
heroku ps:scale web=1
heroku ps:scale bot=1
heroku logs --tail