# Charles&Keith Price Monitoring Bot

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/vladpi/ck-price-monitor-bot)

## Pre-requires

* [Deta](https://www.deta.sh) account (fully free)
* Telegram bot - created through [BotFather](https://t.me/BotFather)
* Your Telegram User ID from [userinfobot](https://t.me/userinfobot)


## Setup

* Start created bot in Telegram via /start command or button
* Deploy application to your Deta project via Deploy to Deta button on top of this readme.
* Fill cron interval, BOT_TOKEN and MY_USER_ID on creation app web page
* Profit!!!


## Editing list of followed products

1. [Install Deta CLI](https://docs.deta.sh/docs/cli/install) for control your project
2. Clone app to local machine via `deta clone --name ck-price-monitor-bot --project default` command (name and project may differ)
3. Change ITEMS var in main.py
4. Deploy changes via `deta deploy` command
5. Proffit!!!