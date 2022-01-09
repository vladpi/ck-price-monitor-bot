import os
import sys

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram.bot import Bot

load_dotenv()

IS_DETA = os.environ.get('DETA_RUNTIME') == 'true'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
MY_USER_ID = os.environ.get('MY_USER_ID')

ITEMS = [
    ('https://www.charleskeith.co.th/th-en/CK2-80270728_TAUPE_S-TH.html', 2590.0),
    ('https://www.charleskeith.co.th/th-en/CK2-20671280_IVORY_S-TH.html', 2790.0),
    ('https://www.charleskeith.co.th/th-en/CK2-40781624_BLACK_L-TH.html', 2990.0),
]


def parse_item_price(url: str) -> float:
    response = httpx.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')
    price_tag = soup.find('meta', {'itemprop': 'price'})

    if price_tag is not None:
        return float(price_tag.attrs.get('content'))

    else:
        raise Exception(f'Цена не найдена на странице: {url}')


def main():
    bot = Bot(BOT_TOKEN)

    try:
        for item_url, item_base_price in ITEMS:
            price = parse_item_price(item_url)
            if price != item_base_price:
                bot.send_message(
                    MY_USER_ID,
                    f'Новая цена на товар!\n{item_base_price:.2f} -> {price:.2f}\n{item_url}',
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
    def check_prices_task(_):
        main()

elif __name__ == '__main__':
    main()
