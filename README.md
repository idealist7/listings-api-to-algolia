# Listings API to Algolia

This project reads the Listings API from [Idealist.org](https://www.idealist.org/)
to keep all of the volunteer listings indexed and up to date in an 
[Algolia](https://www.algolia.com/) index.

## Overview

It's a cron that runs every 20 minutes for up to 17 minutes.
It will progressively populate your index and then keep it up to date.

It's a real project that's suitable for production use,
and it's also an example of how to read the Listings API.

## Deploying

The project includes a `disco.json` file to deploy the project on [Disco](https://disco.cloud).

To deploy on your instance, clone this repo and push to a new private repo that you own.

There are a few env variables that you need to set.

```bash
disco projects:add \
    IDEALIST_AUTH_TOKEN=YOUR_AUTH_TOKEN \
    ALGOLIA_INDEX_NAME=YOUR_ALGOLIA_INDEX_NAME \
    ALGOLIA_APP_ID=YOUR_ALGOLIA_APP_ID \
    ALGOLIA_API_KEY=YOUR_ALGOLIA_API_KEY \
    CRON_ENABLED=true \
    WAIT_SECONDS=0.2 \
    --name idealist-importer
    --github GITHUB_USER/YOUR_REPO
```

Or feel free to adapt your cloned version to deploy where you want.
