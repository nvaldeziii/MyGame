import struct
import json

class MapWriter:
    STRUCT_FORMAT = '<HHII'
    TEST_DIMENTION = 80

    def __init__(self):
        with open('worldmap/map.json', 'r') as mapjson:
            maparr = json.loads(mapjson.read())

        x_len = len(maparr) - 1
        with open('map.bin', 'wb') as bin_out:
            for x in range(0, x_len):
                for y in range(0, x_len):
                    tiledata = maparr[x][y]
                    img = tiledata[0]
                    state = tiledata[1]
                    entry = struct.pack(MapWriter.STRUCT_FORMAT, img, state, y, x)
                    bin_out.write(entry)
                    bin_out.flush()
                    print(f"generating({x},{y})")


if __name__ == '__main__':
    mapwriter = MapWriter()