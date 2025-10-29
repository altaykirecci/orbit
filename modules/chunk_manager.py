import os
import json

class ChunkManager:
    def __init__(self, universe_size, chunk_size=100):
        self.universe_size = universe_size
        self.chunk_size = chunk_size
        self.chunks = {}  # Loaded chunks
        self.loaded_chunks = set()
        self.max_loaded_chunks = 25  # Maximum 5x5 area (500x500)
    
    def get_chunk_coords(self, x, y):
        """Convert coordinates to chunk coordinates"""
        return (x // self.chunk_size, y // self.chunk_size)
    
    def get_chunk_file_path(self, chunk_x, chunk_y, universe_name):
        """Generate chunk file path"""
        return f"universes/{universe_name}/chunk_{chunk_x}_{chunk_y}.json"
    
    def load_chunk(self, chunk_x, chunk_y, universe_name):
        """Load chunk from file"""
        if (chunk_x, chunk_y) in self.loaded_chunks:
            return self.chunks.get((chunk_x, chunk_y), [])
        
        chunk_file = self.get_chunk_file_path(chunk_x, chunk_y, universe_name)
        if os.path.exists(chunk_file):
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunk_data = json.load(f)
                self.chunks[(chunk_x, chunk_y)] = chunk_data
                self.loaded_chunks.add((chunk_x, chunk_y))
                return chunk_data
            except Exception as e:
                print(f"Error loading chunk: {e}")
                return []
        return []
    
    def unload_distant_chunks(self, ship_x, ship_y, max_distance=2):
        """Unload distant chunks from memory"""
        ship_chunk = self.get_chunk_coords(ship_x, ship_y)
        chunks_to_remove = []
        
        for chunk_coord in self.loaded_chunks:
            distance = max(abs(chunk_coord[0] - ship_chunk[0]), 
                          abs(chunk_coord[1] - ship_chunk[1]))
            if distance > max_distance:
                chunks_to_remove.append(chunk_coord)
        
        for chunk_coord in chunks_to_remove:
            if chunk_coord in self.chunks:
                del self.chunks[chunk_coord]
            self.loaded_chunks.remove(chunk_coord)
    
    def get_objects_in_area(self, min_x, min_y, max_x, max_y, universe_name):
        """Return all objects in specified area"""
        objects = []
        
        # Calculate chunks covering this area
        min_chunk_x = min_x // self.chunk_size
        max_chunk_x = max_x // self.chunk_size
        min_chunk_y = min_y // self.chunk_size
        max_chunk_y = max_y // self.chunk_size
        
        # Load each chunk
        for chunk_x in range(min_chunk_x, max_chunk_x + 1):
            for chunk_y in range(min_chunk_y, max_chunk_y + 1):
                chunk_objects = self.load_chunk(chunk_x, chunk_y, universe_name)
                
                # Filter objects in chunk
                for obj in chunk_objects:
                    if (min_x <= obj['x'] <= max_x and 
                        min_y <= obj['y'] <= max_y):
                        objects.append(obj)
        
        return objects
