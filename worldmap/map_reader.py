import struct
from pathlib import Path

from worldmap.map_writer import MapWriter


class MapReader:
    def __init__(self, file):
        # with open(file, "rb") as mapbin:
        #     x=0
        #     while (mapbin.peek(1)):
        #         image = mapbin.read(2).hex()
        #         state = mapbin.read(2).hex()
        #         coord_x = mapbin.read(4).hex()
        #         coord_y = mapbin.read(4).hex()
        #         x+=1
        #         print(f"{x}: {image}, {state}, {coord_x}, {coord_y}")
        #         if x > 20:
        #             break

        struct_size = struct.calcsize(MapWriter.STRUCT_FORMAT)
        struct_unpack = struct.Struct(MapWriter.STRUCT_FORMAT).unpack_from

        self.map_file_size = Path(file).stat().st_size
        self.data = []

        with open(file, "rb") as mapbin:
            read_head = 0
            while True:
                data = mapbin.read(struct_size)
                if not data:
                    break
                read_head += struct_size
                percent = (read_head / self.map_file_size) * 100
                print(f"loading map: {percent}")
                self.data.append(struct_unpack(data))
                # if x > 20:
                #     break


if __name__ == '__main__':
    mapreader = MapReader('map.bin')
