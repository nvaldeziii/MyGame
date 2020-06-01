import json

class GameParams:
    @staticmethod
    def init(file = 'config/config.json'):
        with open(file, 'r') as config_file:
            GameParams.Config = json.loads(config_file.read())
        GameParams.Window.Width = GameParams.Config['Window']['Resolution']['Width']
        GameParams.Window.Height = GameParams.Config['Window']['Resolution']['Height']

    class Window:
        Width = 1280
        Height = 720

        @staticmethod
        def get_tuple_size():
            return (GameParams.Window.Width, GameParams.Window.Height)

        @staticmethod
        def get_aspect():
            return GameParams.Window.Width/GameParams.Window.Height


