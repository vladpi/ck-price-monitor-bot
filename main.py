import os
import sys
from typing import TYPE_CHECKING, Any

import httpx
from bs4 import BeautifulSoup
from deta import Deta
from dotenv import load_dotenv
from telegram.bot import Bot

if TYPE_CHECKING:
    from deta import Base

load_dotenv()

IS_DETA = os.environ.get('DETA_RUNTIME') == 'true'

DETA_PROJECT_KEY = os.environ.get('DETA_PROJECT_KEY')
DETA_DB_NAME = os.environ.get('DETA_DB_NAME', 'ck-items-local')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
MY_USER_ID = os.environ.get('MY_USER_ID')

EXAMPLE_ITEM_KEY = 'EXAMPLE_ITEM'
EXAMPLE_ITEM = {
    'key': EXAMPLE_ITEM_KEY,
    'url': 'https://www.charleskeith.co.th/th-en/CK2-80270728_TAUPE_S-TH.html',
    'base_price': 2590.0,
    'user_id': MY_USER_ID,
}


def parse_item_price(url: str) -> float:
    response = httpx.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')
    price_tag = soup.find('meta', {'itemprop': 'price'})

    if price_tag is not None:
        return float(price_tag.attrs.get('content'))

    else:
        raise Exception(f'Цена не найдена на странице: {url}')


def init_deta_db(deta: Deta) -> 'Base':
    db = deta.Base(DETA_DB_NAME)

    if db.fetch().count == 0:
        db.put(data=EXAMPLE_ITEM_KEY)

    return db


def main() -> None:
    bot = Bot(BOT_TOKEN)
    db = init_deta_db(Deta(DETA_PROJECT_KEY))
    items = db.fetch().items

    try:
        for item in items:
            url = item['url']
            base_price = item['base_price']
            price = parse_item_price(url)
            if price != item['base_price']:
                bot.send_message(
                    MY_USER_ID,
                    f'Новая цена на товар!\n{base_price:.2f} -> {price:.2f}\n{url}',
                )

    except Exception as ex:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        bot.send_message(
            MY_USER_ID,
            f'Что-то пошло не так.\nОшибка {exc_type} {fname}:{exc_tb.tb_lineno}\n{ex}',
        )

        raise ex


if IS_DETA:
    from deta import app

    @app.lib.cron()
    def check_prices_task(event: Any) -> None:
        main()

elif __name__ == '__main__':
    main()
