
import json
import requests
import configparser as cfg

CONFIG_FILE = "config.cfg"

class telegram_bot():
    
    def __init__(self, config):
        self.parser = cfg.ConfigParser(CONFIG_FILE)
        self.token = self.read_token_from_config()
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset = None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        response = requests.get(url)
        return json.loads(response.content)
    
    def send_message(self, message, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, message)
        if message is not None:
            requests.get(url)

    def read_token_from_config(self):
        return self.parser.get('credentials', 'token')

    def error_msg(self):
        return self.parser.get('messages', 'error_msg')

    def start_message(self):
        return self.parser.get('messages', 'first_message')