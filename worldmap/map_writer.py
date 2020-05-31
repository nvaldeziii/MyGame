import struct


class MapWriter:
    STRUCT_FORMAT = '<HHII'
    def __init__(self):
        with open('map.bin', 'wb') as bin_out:
            for x in range(0, 255):
                for y in range(0, 255):
                    entry = struct.pack(MapWriter.STRUCT_FORMAT, 1, 0, x, y)
                    bin_out.write(entry)
                    bin_out.flush()
                    print(f"generating({x},{y})")


if __name__ == '__main__':
    mapwriter = MapWriter()