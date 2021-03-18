#!/bin/bash
heroku login
heroku git:remote -a yt-shevchenko
heroku stack:set container
git push heroku master
heroku ps:scale api=1
heroku ps:scale bot=1