
import configparser as cfg
from main import telegram_bot


def TEST_send_reply(message):
    reply = "Got you, please wait"
    return reply

def start_message(msg_cfg, message):
    parser = cfg.ConfigParser()
    parser.read(msg_cfg)
    return parser.get('firstmessage', 'fmsg')

def search(msg_cfg, message):
    parser = cfg.ConfigParser()
    parser.read(msg_cfg)
    manufacturer = parser.get('search', 'manufacturer')
    model = parser.get('search', 'model')

if __name__=='__main__':
    msg_cfg = "messages.cfg"
    bot = telegram_bot("config.cfg")
    update_id = None

    while True:
        updates = bot.get_updates(offset = update_id)
        print(updates)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    message = item["message"]["text"]
                    if message == "search":
                        reply = search(msg_cfg, message)
                except:
                    message = None
                    reply = error_msg(msg_cfg, message)
                    
                from_user = item["message"]["from"]["id"]
                reply = start_message(msg_cfg, message)
                bot.send_message(reply, from_user)