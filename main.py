# from fake_useragent import UserAgent
import time
import telebot
from bot import TOKEN
from bot import Parser_Bot
from telebot import types
from bot import too_many_requests

# user_agent = UserAgent()

with open("data.txt", 'r') as file_:
    accessing_list = file_.readlines()


# headers_ = {"Accept": '*/*',
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                           "Chrome/105.0.0.0 Safari/537.36"}


def telegram_bot(token):
    bot = telebot.TeleBot(token, parse_mode='Markdown')
    stopped = False
    interval = [1, 244]
    benefit = 0
    profit = 0

    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_execute = types.KeyboardButton("execute ✅")
    button_stop = types.KeyboardButton("stop ❌")
    button_info = types.KeyboardButton("info ❓")
    button_settings = types.KeyboardButton("/settings")
    main_markup.add(button_execute, button_stop, button_info, button_settings)

    settings_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_interval = types.KeyboardButton("parsing interval")
    button_benefit = types.KeyboardButton("benefit filter")
    button_profit = types.KeyboardButton("profit filter")
    button_return = types.KeyboardButton("return")
    settings_markup.add(button_interval, button_benefit, button_profit, button_return)

    cancel_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_markup.add(button_return)

    with open('data.txt', 'r') as data:
        data_listing = data.readlines()
        for chat_id in data_listing:
            bot.send_message(chat_id,
                             text="hello, I'm Parser_bot, which was written by @Dmitry_zb 😎\n"
                             "I can Parse useful data from Steam Market to you :)",
                             reply_markup=main_markup)
    data.close()

    # Start Function
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        # with open('data.txt', 'w') as file:
        #     file.write(str(message.chat.id))
        # file.close()
        with open('data.txt', 'r+') as file:
            listing = file.readlines()
            if not listing.count(str(message.chat.id)):
                file.write(message.chat.id)
        file.close()

        if not accessing_list.count(user_id):
            bot.send_message(message.chat.id,
                             text="Unfortunately you don't have rights "
                                  "for using this bot ☹️")
            return
        bot.send_message(message.chat.id,
                         text="hello, I'm Parser_bot, which was written by @Dmitry_zb 😎\n"
                              "I can Parse useful data from Steam Market to you :)",
                         reply_markup=main_markup)

    # Stop Function
    @bot.message_handler(commands=['stop'])
    def stop(message):
        bot.send_message(message.chat.id,
                         text="successfully stopped!\n"
                              "GG WP")
        bot.stop_polling()

    # Settings Function
    @bot.message_handler(commands=['settings', 'return'])
    def settings(message):
        bot.send_message(message.chat.id,
                         text="chose what you wanna do:\n"
                              "press button: \"parsing interval\" to set page interval of searching\n"
                              "press button: \"benefit filter\" to set percentage benefit filter\n"
                              "press button: \"profit filter\" to set currency profit filter",
                         reply_markup=settings_markup)
        bot.register_next_step_handler(message, handler)

    # Settings Handler
    def handler(message):
        if message.text == "parsing interval":
            bot.send_message(message.chat.id,
                             text="send interval of page-parsing. . .\n"
                                  "(example: 1, 10)",
                             reply_markup=cancel_markup)
            bot.register_next_step_handler(message, change_interval)
        elif message.text == "benefit filter":
            bot.send_message(message.chat.id,
                             text="send minimal benefit percentage. . .\n"
                                  "(example: 10)",
                             reply_markup=cancel_markup)
            bot.register_next_step_handler(message, change_benefit)
        elif message.text == "profit filter":
            bot.send_message(message.chat.id,
                             text="send minimal trade profit. . .\n"
                                  "(example: 10)", parse_mode='Markdown',
                             reply_markup=cancel_markup)
            bot.register_next_step_handler(message, change_profit)
        elif message.text == "return":
            bot.send_message(message.chat.id,
                             text="returned",
                             reply_markup=main_markup)
            return
        else:
            bot.send_message(message.chat.id,
                             text="wrong command!",
                             reply_markup=main_markup)
            return

    # Set parse interval
    def change_interval(message):
        nonlocal interval
        try:
            answer = message.text
            if answer.strip() == "return":
                bot.send_message(message.chat.id,
                                 text="returned",
                                 reply_markup=main_markup)
                return
            interval = answer.split(',')
            if len(interval) != 2:
                raise Exception
            interval[0] = int(interval[0].strip())
            interval[1] = int(interval[1].strip()) + 1
            if interval[0] < 1:
                raise Exception

            # for csgo:
            # if interval[1] > 1801:
            #     raise Exception
            if interval[0] > interval[1]:
                raise Exception
            bot.send_message(message.chat.id, f"success, new interval: [{interval[0]}, {interval[1] - 1}]",
                             reply_markup=main_markup)
        except Exception as ex:
            bot.send_message(message.chat.id, "unexpected error: " + str(ex) + "❗️",
                             reply_markup=main_markup)

    # Set benefit filter
    def change_benefit(message):
        nonlocal benefit
        try:
            answer = message.text
            if answer.strip() == "return":
                bot.send_message(message.chat.id,
                                 text="returned",
                                 reply_markup=main_markup)
                return
            benefit = float(answer.strip())
            bot.send_message(message.chat.id, f"success, new benefit filter: {benefit}%",
                             reply_markup=main_markup)
        except Exception as ex:
            bot.send_message(message.chat.id, "unexpected error: " + str(ex) + "❗️",
                             reply_markup=main_markup)

    # Set profit filter
    def change_profit(message):
        nonlocal profit
        try:
            answer = message.text
            if answer.strip() == "return":
                bot.send_message(message.chat.id,
                                 text="returned",
                                 reply_markup=main_markup)
                return
            profit = float(answer.strip())
            bot.send_message(message.chat.id, f"success, new profit filter: {profit} rub.",
                             reply_markup=main_markup)
        except Exception as ex:
            bot.send_message(message.chat.id, "unexpected error: " + str(ex) + "❗️",
                             reply_markup=main_markup)

    # User text messages handler
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        nonlocal stopped
        retry = 0
        if message.text.lower() == 'execute ✅':
            stopped = False
            bot.send_message(message.chat.id, "success, start searching. . .")
            try:
                counter = 0
                for page in range(interval[0], interval[1]):
                    if stopped:
                        break
                    Parser_Bot(page, bot, message, benefit, profit)
                    # success = False
                    # while not success:
                    #     try:
                    #         Parser_Bot(page, bot, message, benefit, profit)
                    #         success = True
                    #     except Exception as ex:
                    #         if retry == 4:
                    #             bot.send_message(message.chat.id,
                    #                              f"Unexpected Error: parsing page {page} error: {ex}")
                    #             retry = 0
                    #             break
                    #         retry += 1
                    #         bot.send_message(message.chat.id,
                    #                          f"Unexpected Error: parsing page {page} retry: {retry}")
                    #         time.sleep(60)
                    global too_many_requests
                    if too_many_requests[0]:
                        stopped = True
                        too_many_requests[0] = False
                    counter += 1
                    if not counter % 2 and counter != interval[1] - interval[0]:
                        bot.send_message(message.chat.id, f"page {page}, cool down. . .")
                        time.sleep(240)
                        bot.send_message(message.chat.id, "success, start searching. . .")
                bot.send_message(message.chat.id, "execute command was completed!")
            except Exception as ex:
                bot.send_message(message.chat.id, "unexpected:\n" + str(ex) + "❗️")
        elif message.text.lower() == 'stop ❌':
            stopped = True
            bot.send_message(message.chat.id, "I will stop after load this page!")
        elif message.text.lower() == 'info ❓':
            bot.send_message(message.chat.id, "I can do many things, just ask me!\n"
                                              "Commands:\n"
                                              "/start\t-\tsay hello\n"
                                              "/stop\t-\tsay goodbye\n"
                                              "/settings\t-\tgo to my settings\n"
                                              "Buttons:\n"
                                              "info\t-\tyou already here\n"
                                              "execute\t-\tstart parsing data\n"
                                              "stop\t-\tstop parsing data\n"
                                              f"\nbenefit filter: {benefit}%\n"
                                              f"profit filter: {profit} rub.\n"
                                              f"parsing interval: [[ {interval[0]}, {interval[1] - 1} ]]")
        else:
            bot.send_message(message.chat.id, "Wrong command. . . ☹️")

    bot.polling()


# Program enter point
if __name__ == '__main__':
    telegram_bot(TOKEN)
