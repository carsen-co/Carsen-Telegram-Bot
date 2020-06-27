
import os
import csv
import time
import threading
import configparser as cfg

from search_module import search
from telegram_bot import telegram_bot

global msg_cfg
msg_cfg =  "messages.cfg"


class SEARCH():
    
    def input_wait(self, msg_cfg):
        while True:
            updates = bot.get_updates(offset = update_id)
            print(updates)
            updates = updates["result"]
            if updates:
                messages = []
                for item in updates:
                    try:
                        message = item["message"]["text"]
                        messages.append(message)
                    except:
                        message = None
                return messages[-1]
    
    def manufacturer(self, msg_cfg):
        parser = cfg.ConfigParser()
        parser.read(msg_cfg)
        return parser.get('search', 'manufacturer')
    
    def model(self, msg_cfg):
        parser = cfg.ConfigParser()
        parser.read(msg_cfg)
        return parser.get('search', 'model')

    def __init__(self, msg_cfg):        
        from_user = item["message"]["from"]["id"]
        bot.send_message(self.manufacturer(msg_cfg), from_user)
        inp_make = self.input_wait(msg_cfg)
        
        update_id = None
        bot.send_message(self.model(msg_cfg), from_user)
        while True:
            inp_model = self.input_wait(msg_cfg)
            print(inp_make, inp_model)
            time.sleep(1)
            if not inp_model == inp_make:
                break
        
        bot.send_message("Working, please wait...", from_user)

        chat_input = [inp_make, inp_model]
        for i in range(9):
            chat_input.append("")
        filename = search(os.getcwd(), chat_input)

        maindir = os.getcwd()
        os.chdir("./csv files")
        with open(filename, mode="r", newline='') as datafile:
            datareader = csv.reader(datafile)
            data = list(datareader)
            data.pop(0)
        
        data_lists = []
        for ditem in data:
            for i in range(len(ditem)):
                try:
                    data_lists[i].append(ditem[i])
                except:
                    data_lists.append([])
                    data_lists[i].append(ditem[i])

        ind = data_lists[6].index(max(data_lists[6]))
        print(data_lists[0][ind])
        bot.send_message("Here is the best listing I could find: "+data_lists[0][ind], from_user)

        os.remove(filename)
        os.chdir(maindir)

if __name__=='__main__':
    bot = telegram_bot("config.cfg")
    update_id = None

    while True:
        updates = bot.get_updates(offset = update_id)
        print(updates)
        updates = updates["result"]
        if updates:
            messages = []
            for item in updates:
                update_id = item["update_id"]
                from_user = item["message"]["from"]["id"]
                try:
                    message = item["message"]["text"]
                    messages.append(message)
                    if messages[-1].lower() == "search":
                        thread = threading.Thread(target = SEARCH, args = ("messages.cfg",))
                        thread.start()
                        thread.join()
                    else:
                        reply = bot.start_message()
                        bot.send_message(reply, from_user)

                except Exception as e:
                    print(e)
                    message = None
                    reply = bot.error_msg()
                    bot.send_message(reply, from_user)
