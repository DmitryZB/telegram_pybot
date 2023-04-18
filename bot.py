import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent


too_many_requests = [False]
TOKEN = "5769190272:AAG75MUv1hyZnTyI3O47rIdakbFSVsXcZfE"
# user_agent = UserAgent()


# Function of parsing links on items on Steam market
def Parser_Bot(page, bot_, message_, benefit, profit):
    options = webdriver.ChromeOptions()
    # user_agent_ = user_agent.random
    user_agent_ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument(f"user_agent ={user_agent_}")
    # s = Service("C:\\Users\\SkyNet\\Desktop\\PYTHON\\chromedriver.exe")

    driver = webdriver.Chrome(options=options)
    headers_ = {"Accept": '*/*',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/105.0.0.0 Safari/537.36"}

    try:

        req = requests.get(
            # sorted by popularity
            url=f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count={10}&search_"
                f"descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_"
                f"ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_"
                f"StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any",

            # sorted by quantity
            # url=f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count=10&search_"
            #     f"descriptions=0&sort_column=quantity&sort_dir=desc&appid=730&category_730_"
            #     f"ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_"
            #     f"StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any",

            # sorted by price
            # url=f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count=10"
            #     f"&search_descriptions=0&sort_column=price&sort_dir=asc&appid=730",
            # url=f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count=10&search_"
            #     f"descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_"
            #     f"ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_"
            #     f"StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any",

            # knifes
            # url=f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count=10&search_"
            # f"descriptions=0&sort_column=price&sort_dir=asc&appid=730&category_730_"
            # f"ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_"
            # f"StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_"
            # f"Type%5B%5D=tag_CSGO_Type_Knife",

            # dota
            # url=
            # f"https://steamcommunity.com/market/search/render/?query=&start={page - 1}0&count=10"
            # f"&search_descriptions=0&sort_column=price&sort_dir=asc&appid=570",

            headers=headers_)

        data = req.json()
        parse = BeautifulSoup(data['results_html'], "lxml")
        market_refs = parse.find_all(class_="market_listing_row_link")
        for item in market_refs:
            item_href = item.get("href")
            name = item.find("span", class_="market_listing_item_name")
            driver.get(url=item_href)
            time.sleep(0.5)
            data = driver.page_source
            index1 = data.find("Market_LoadOrderSpread") + 24
            index2 = index1
            while data[index2] != ' ':
                index2 += 1
            item_id = int(data[index1:index2:])
            Scanner(url_=f"https://steamcommunity.com/market/itemordershistogram?country=RU&language="
                         f"russian&currency=5&item_nameid={item_id}&two_factor=0",
                    name=name.text,
                    href=item_href,
                    ua=user_agent_,
                    bot_=bot_,
                    message_=message_,
                    page_=page,
                    benefit_=benefit,
                    profit_=profit)
            if too_many_requests[0]:
                break
    except ValueError as ex:
        bot_.send_message(message_.chat.id, f"Unexpected Error: parsing page {page} error: {ex}")
    except Exception as ex:
        bot_.send_message(message_.chat.id, f"Unexpected Error: parsing page {page} error: {ex}")
    finally:
        driver.close()
        driver.quit()


# Function of parsing data of each skin
def Scanner(url_, name, href, ua, bot_, message_, page_, benefit_, profit_):
    try:
        headers_ = {
            "User-Agent": ua
        }
        name = str(name)

        # steam parse
        response_ = requests.get(url=url_, headers=headers_)
        if response_.status_code == 429:
            bot_.send_message(message_.chat.id, f"To many requests, take a pause...")
            global too_many_requests
            too_many_requests[0] = True
            return
        data = response_.json()
        try:
            buy_order = BeautifulSoup(data['buy_order_summary'], "lxml")
            buy_order = buy_order.text
        except ValueError:
            bot_.send_message(message_.chat.id, f"No buy order for: \"{name}\"")
            return
        summary_buy_order = buy_order[:buy_order.find("Начальная цена: "):]
        buy_order = buy_order[buy_order.find("Начальная цена: ") + 16::]
        buy_order = buy_order[:-5:]

        sell_order = BeautifulSoup(data['sell_order_summary'], "lxml")
        sell_order = sell_order.text
        summary_sell_order = sell_order[:sell_order.find("Начальная цена: "):]
        sell_order = sell_order[sell_order.find("Начальная цена: ") + 16::]
        sell_order = sell_order[:-5:]

        money_rise = float(sell_order.replace(',', '.')) * 0.87 - float(buy_order.replace(',', '.'))
        percentage = money_rise/float(buy_order.replace(',', '.')) * 100
        if percentage >= benefit_ \
                and money_rise >= profit_ \
                and int(summary_sell_order[summary_sell_order.find(': ') + 1:]) >= 10:
            message_text = f"Name: "\
                           f"{name}\n"\
                           f"Page: "\
                           f"{page_}\n"\
                           f"Buy orders count: "\
                           f"{summary_buy_order[summary_buy_order.find(': ') + 1:]}\n"\
                           f"Sell orders count: "\
                           f"{summary_sell_order[summary_sell_order.find(': ') + 1:]}\n"\
                           f"Profit: "\
                           f"{'%.2f' % money_rise} rub.\n"\
                           f"Percentage: "\
                           f"{'%.2f' % percentage}%\n"\
                           f"Steam price: "\
                           f"{buy_order} rub.\n"\
                           f"Link in Steam: "\
                           f"{href}"
            bot_.send_message(message_.chat.id, message_text)
        time.sleep(1)
    except ValueError as ex:
        bot_.send_message(message_.chat.id, f"Unexpected Error: parsing \"{name}\" item error: {ex}")
    except Exception as ex:
        bot_.send_message(message_.chat.id, f"Unexpected Error: parsing \"{name}\" item error: {ex}")
