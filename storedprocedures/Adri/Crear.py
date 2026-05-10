import json
import pyodbc
import os

class ConexionBaseDatos:
    def __init__(self, nombre_archivo):
        # Localiza el JSON automáticamente donde esté el script
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
        self.datos_conexion = self._leer_config()

    def _leer_config(self):
        try:
            if not os.path.exists(self.ruta_archivo):
                print(f"\n[!] ERROR: No se encontró el archivo en: {self.ruta_archivo}")
                return None
            with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error crítico al leer el JSON: {e}")
            return None

    def obtener_conexion(self):
        if not self.datos_conexion: return None
        try:
            cadena = (
                f"DRIVER={self.datos_conexion['driver']};"
                f"SERVER={self.datos_conexion['server']};"
                f"DATABASE={self.datos_conexion['database']};"
                f"Trusted_Connection={self.datos_conexion['trusted_connection']};"
            )
            return pyodbc.connect(cadena)
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None

class GestorCanciones:
    def __init__(self, db):
        self.db = db

    def obtener_id_album_por_nombre(self, nombre_album):
        # Búsqueda por tituloAlbum en Catalogo.Album
        sql_busqueda = "SELECT idAlbum FROM Catalogo.Album WHERE UPPER(tituloAlbum) = UPPER(?)"
        conn = self.db.obtener_conexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_busqueda, (nombre_album.strip(),))
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None
            except Exception as e:
                print(f"Error al buscar álbum: {e}")
                return None
            finally:
                conn.close()
        return None

    def agregar_cancion(self):
        if not self.db.datos_conexion: return

        print("\n--- REGISTRO DE NUEVA CANCIÓN ---")
        nombre = input("Nombre de la canción *: ")
        duracion = input("Duración en segundos *: ")
        lanzamiento = input("Fecha lanzamiento (AAAA-MM-DD) *: ")
        
        # IMPORTANTE: Según tu CHECK debe ser 'activa', 'inactiva', 'eliminada' o 'bloqueada'
        estado_raw = input("Estado (ej. activa, inactiva) *: ")
        estado = estado_raw.strip().lower() 
        
        calidad = input("Calidad Kbps *: ")
        nombre_album = input("Nombre del Álbum *: ")
        album_id = self.obtener_id_album_por_nombre(nombre_album)

        if album_id is None:
            print(f"\n[!] Error: El álbum '{nombre_album}' no existe.")
            return

        letra = input("Letra (Enter para omitir): ")
        pista = input("Número de pista (Enter para omitir): ")

        if not all([nombre, duracion, lanzamiento, estado, calidad]):
            print("\n[!] Error: Faltan campos obligatorios.")
            return

        sql_insert = """
            INSERT INTO Catalogo.Cancion 
            (nombreCancion, duracion, fechaLanzamiento, estadoCancion, calidadKbps, totalReproducciones, letraCancion, Album_idAlbum, numeroPista)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?)
        """
        
        conn = self.db.obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql_insert, (
                    nombre, 
                    int(duracion), 
                    lanzamiento, 
                    estado, 
                    int(calidad), 
                    letra.strip() if letra.strip() else None, 
                    album_id, 
                    int(pista) if pista.strip() else None
                ))
                conn.commit()
                print(f"\n[OK] Canción '{nombre}' guardada con éxito.")
                print(f"Estado registrado: {estado}")
            except Exception as e:
                print(f"\n[X] Error al insertar: {e}")
            finally:
                conn.close()

if __name__ == "__main__":
    app = GestorCanciones(ConexionBaseDatos('config.json'))
    app.agregar_cancion()