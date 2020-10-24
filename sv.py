
import time, threading
import configparser as cfg

from telegram_bot import telegram_bot
from mobile_de.methods import surface_search

class SEARCH():
    def input_wait(self, offset_update):
        update_id = offset_update
        while True:
            updates = bot.get_updates(offset = update_id)
            updates = updates["result"]
            if updates:
                for item in updates:
                    update_id = item["update_id"]
                    from_user = item["message"]["from"]["id"]
                    message = item["message"]["text"]
                    if message.lower() == "blank":
                        message = ""
                    return message, update_id

    def __init__(self, entry_update):            
        bot.send_message(bot.parser.get('messages', 'manufacturer'), from_user)
        inp_make, entry_update = self.input_wait(entry_update)

        bot.send_message(bot.parser.get('messages', 'model'), from_user)
        inp_model, entry_update = self.input_wait(entry_update)

        bot.send_message(bot.parser.get('messages', 'budget'), from_user)
        inp_budget, entry_update = self.input_wait(entry_update)
        inp_budget = [int(inp_budget)-(int(inp_budget)/10), int(inp_budget)+(int(inp_budget)/10)]

        bot.send_message("Working, please wait...", from_user)

        chat_input = [inp_make, inp_model, inp_budget[0], inp_budget[1], '', '', '', '']
        data = surface_search(chat_input)

        scores = [d[5] for d in data]

        bot.send_message("Here is the best listing I could find: " + data[scores.index(max(scores))][0], from_user)

if __name__=='__main__':
    bot = telegram_bot()
    update_id = None

    while True:
        updates = bot.get_updates(offset = update_id)
        print(updates)
        updates = updates["result"]
        if updates:
            stspam = 0
            messages = []
            for item in updates:
                update_id = item["update_id"]
                from_user = item["message"]["from"]["id"]
                message = item["message"]["text"]
                messages.append(message)
                if messages[-1].lower() == "search":
                    thread = threading.Thread(target = SEARCH, args = (update_id, ))
                    thread.start()
                    thread.join()
                elif stspam != 1:
                    stspam = 1
                    bot.send_message(bot.start_message(), from_user)
