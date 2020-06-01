import math

class MouseClick:
    @staticmethod
    def get_angle_from_player(playerpos, mousepos):
        delta_x = mousepos[0] - playerpos[0]
        delta_y = playerpos[1] - mousepos[1]
        return math.atan2(delta_y, delta_x)

    @staticmethod
    def get_angle_from_player2(playerpos, mousepos):
        delta_x = mousepos[0] - playerpos[0]
        delta_y = playerpos[1] - mousepos[1]
        return math.atan(delta_y/delta_x)