import random
import time
import struct
import math

import shapes 

def rand_pos_neg(amplitude):
    return (random.random() - .5) * 2. * amplitude

class VoronoiChunkGenerator:
    def __init__(self, density):
        self.density = density

    def new_chunk(self, key):
        x, y = key
        ret = set()

        N = int(math.sqrt(self.density))

        for j in range(N):
            dy = (j + 0.5) / N
            for i in range(N):
                dx = (i + 0.5) / N
                ret |= {(x + dx + rand_pos_neg(0.45) / N,
                         y + dy + rand_pos_neg(0.45) / N)}
        return ret

class VoronoiChunkDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.index = dict()
        self.index_offset = 0
        
        try:
            with open(filename, "rb") as f:
                self._load_seed(f)
                self._load_index(f)
        except FileNotFoundError:
            with open(filename, "wb") as f:
                self._create_seed()
                self._save_seed(f)
                self._save_empty_index(f)

    def load(self, key):
        if not key in self.index.keys():
            return None

        with open(self.filename, "rb") as f:
            return self._load_chunk(f, key)

    def save(self, key, chunk):
        with open(self.filename, "rb+") as f:
            if key not in self.index.keys():
                self._create_index(key, f)

            self._save_chunk(f, key, chunk)

    def _create_index(self, key, f):
        # 1. Create new entry
        self.index[key] = self._next_offset()

        # 2. Update index offset
        self.index_offset += 1 + 8*16 # sizeof(chunk) TODO change

        # 3. Save index back
        self._save_index(f)

    def _create_seed(self):
        self.seed = int(time.time())

    def _load_seed(self, f):
        f.seek(0)
        self.seed = int.from_bytes(f.read(4), byteorder = "little", signed = False)

    def _save_seed(self, f):
        f.seek(0)
        f.write(self.seed.to_bytes(4, byteorder = "little", signed = False))

    def _save_empty_index(self, f):
        self.index_offset = 8
        self._save_index(f)

    def _load_index(self, f):
        f.seek(4)
        self.index_offset = int.from_bytes(f.read(4), byteorder = "little", signed = False)

        f.seek(self.index_offset)
        n_entries = int.from_bytes(f.read(4), byteorder = "little", signed = False)

        for i in range(n_entries):
            x = int.from_bytes(f.read(4), byteorder = "little", signed = True)
            y = int.from_bytes(f.read(4), byteorder = "little", signed = True)
            offset = int.from_bytes(f.read(4), byteorder = "little", signed = False)
            
            self.index[x, y] = offset

    def _save_index(self, f):
        f.seek(4)
        f.write(self.index_offset.to_bytes(4, byteorder = "little", signed = False))
            
        f.seek(self.index_offset)
        n_entries = len(self.index.keys())

        # n_entries
        f.write(n_entries.to_bytes(4, byteorder = "little", signed = False))

        keys = set(self.index.keys())
        for i in range(n_entries):
            x, y = keys.pop()
            f.write(x.to_bytes(4, byteorder = "little", signed = True))
            f.write(y.to_bytes(4, byteorder = "little", signed = True))
            f.write(self.index[x, y].to_bytes(4, byteorder = "little", signed = False))

    def _load_chunk(self, f, key):
        x, y = key

        offset = self.index[key]
        f.seek(offset)

        n_points = int.from_bytes(f.read(1), byteorder = "little", signed = False)

        chunk = set()

        for i in range(n_points):
            local_x = struct.unpack("f", f.read(4))[0]
            local_y = struct.unpack("f", f.read(4))[0]
            chunk |= {(x + local_x, y + local_y)}
        return chunk

    def _save_chunk(self, f, key, chunk):
        x, y = key

        offset = self.index[key]
        f.seek(offset)

        # n_points
        f.write(len(chunk).to_bytes(1, byteorder = "little", signed = False))

        copy = set(chunk)
        while len(copy) > 0:
            total_x, total_y = copy.pop()
            local_x = total_x - x
            local_y = total_y - y
            f.write(bytearray(struct.pack("f", local_x)))
            f.write(bytearray(struct.pack("f", local_y)))

    def _next_offset(self):
        return self.index_offset
        LEN_SEED = 4
        LEN_INDEX_OFFSET = 4
        LEN_CHUNKS = (1 + 8 * 16) * len(self.index.keys()) # TODO: change!
        return LEN_SEED + LEN_INDEX_OFFSET + LEN_CHUNKS

class VoronoiExplorer:
    def __init__(self, filename, density):
        self.chunk_generator = VoronoiChunkGenerator(density)
        self.chunk_database = ChunkDatabase(filename)
        self.chunk_manager = chunk.ChunkManager(self.chunk_generator, self.chunk_database)

        self.pointset = shapes.PointSet()

    def load_chunk(self, key):
        is_new_chunk, chunk = self.chunk_manager.load_chunk(key)

        if is_new_chunk:
            for point in chunk:
                self.pointset.add_point(point)

    def unload_chunk(self, key):
        chunk = self.chunk_manager.unload_chunk(key)

    def keep_only_chunks(self, keys):
        self.chunk_manager.keep_only_chunks(keys)
