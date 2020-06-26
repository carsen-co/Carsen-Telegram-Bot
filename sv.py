
import time
import threading
import configparser as cfg
from telegram_bot import telegram_bot

global msg_cfg
msg_cfg =  "messages.cfg"

def TEST_send_reply():
    reply = "Got you, please wait"
    return reply

def start_message(msg_cfg):
    parser = cfg.ConfigParser()
    parser.read(msg_cfg)
    return parser.get('firstmessage', 'fmsg')

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


if __name__=='__main__':
    bot = telegram_bot("config.cfg")
    update_id = None

    while True:
        updates = bot.get_updates(offset = update_id)
        print(updates)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                from_user = item["message"]["from"]["id"]
                try:
                    message = item["message"]["text"]
                    if message.lower() == "search":
                        thread = threading.Thread(target = SEARCH, args = ("messages.cfg",))
                        thread.start()
                        thread.join()
                    else:
                        reply = start_message(msg_cfg)
                        bot.send_message(reply, from_user)

                except Exception as e:
                    print(e)
                    message = None
                    reply = bot.error_msg(msg_cfg)
                    bot.send_message(reply, from_user)
