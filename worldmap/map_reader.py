import struct
import logging
import json
from pathlib import Path

from worldmap.map_writer import MapWriter


logger = logging.getLogger()


class MapReader:
    def __init__(self):
        self.data = [[0]*1]*1
        self.dimention = 0
        # data format
        #  [
        #     FFFF, <- image id
        #     FFFF, <- state
        #     FFFF, <- object id
        #   ]

    @staticmethod
    def tile_disector(tiledata, x ,y):
        data = {
            'tile_id': '0000',
            'tile_state': '0',
            'obj_id': '0000',
            'obj_state': '0',
            'group' : '0'
        }
        try:
            data['tile_id'] = f'{tiledata[0]:04x}'
            data['tile_state'] = f'{tiledata[1]:x}'
        except IndexError as e:
            logger.warning(f"failed to load tile data on ({x},{y}): {e}")

        try:
            data['obj_id'] = f'{tiledata[2]:04x}'
            data['obj_state'] = f'{tiledata[3]:x}'
        except IndexError as e:
            logger.warning(f"failed to load obj data on ({x},{y}): {e}")

        data['group'] = f'{tiledata[4]:x}'

        return data

    def from_json(self, file):
        logger.debug("loading map data")
        with open('worldmap/map.json', 'r') as mapjson:
            self.data = json.loads(mapjson.read())
            self.lenght = len(self.data) - 1
            self.height = len(self.data[0]) - 1
        logger.debug("done...")

    # def from_binary(self, file):
    #     struct_size = struct.calcsize(MapWriter.STRUCT_FORMAT)
    #     struct_unpack = struct.Struct(MapWriter.STRUCT_FORMAT).unpack_from
    #     self.map_file_size = Path(file).stat().st_size
    #     with open(file, "rb") as mapbin:
    #         read_head = 0
    #         while True:
    #             data = mapbin.read(struct_size)
    #             if not data:
    #                 break
    #             read_head += struct_size
    #             percent = (read_head / self.map_file_size) * 100
    #             print(f"loading map: {percent}")
    #             self.data.append(struct_unpack(data))
    #     self.dimention = len(self.data)


if __name__ == '__main__':
    mapreader = MapReader()
