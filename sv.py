
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
                    return message, update_id

    def manufacturer(self):
        return bot.parser.get('messages', 'manufacturer')

    def model(self):
        return bot.parser.get('messages', 'model')

    def __init__(self, make_entry_update):            
        bot.send_message(self.manufacturer(), from_user)
        inp_make, model_entry_update = self.input_wait(make_entry_update)

        bot.send_message(self.model(), from_user)
        inp_model, sample_entry_update = self.input_wait(model_entry_update)

        bot.send_message("Working, please wait...", from_user)

        chat_input = [inp_make, inp_model, '', '', '', '', '', '']
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
