import json

class GameParams:
    initiated = False
    @classmethod
    def init(cls, file='config/config.json', re_init=False):
        if not cls.initiated or re_init:
            with open(file, 'r') as config_file:
                cls.config = json.loads(config_file.read())

            cls.init_window()
            cls.initiated = True

    @classmethod
    def init_window(cls):
        cls.window = cls.config['window']
        cls.window_tuple = (
            cls.config['window']['resolution']['width'],
            cls.config['window']['resolution']['height']
        )

GameParams.init()
