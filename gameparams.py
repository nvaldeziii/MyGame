class GameParams:
    class Window:
        Width = 1280
        Height = 720

        @staticmethod
        def get_tuple_size():
            return (GameParams.Window.Width, GameParams.Window.Height)

        @staticmethod
        def get_aspect():
            return GameParams.Window.Width/GameParams.Window.Height
