class Cancion:
    def __init__(self, nombre, duracion, fecha, 
                 estado, calidad, album_id, pista=None):
        self.nombre    = nombre
        self.duracion  = duracion
        self.fecha     = fecha
        self.estado    = estado
        self.calidad   = calidad
        self.album_id  = album_id
        self.pista     = pista

    def __str__(self):
        return (f"Cancion | Nombre: {self.nombre} | "
                f"Duración: {self.duracion}s | "
                f"Estado: {self.estado} | "
                f"Calidad: {self.calidad}kbps")