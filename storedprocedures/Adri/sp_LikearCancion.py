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

class BibliotecaMusical:
    def __init__(self, db):
        self.db = db

    def listar_canciones_like(self):
        print("\n--- CONSULTAR CANCIONES FAVORITAS (LIKE) ---")
        
        # Pedimos el ID del usuario por consola (como pide tu tarea con input)
        id_usuario = input("Ingrese el ID del Usuario a consultar: ")

        if not id_usuario.isdigit():
            print("[!] Error: El ID debe ser un número entero.")
            return

        conn = self.db.obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Ejecutamos el Stored Procedure usando el parámetro capturado
                # La sintaxis '{CALL nombre_sp (?)}' es la más estándar para procedimientos
                sql_sp = "{CALL Biblioteca.sp_ListarCancionesLike (?)}"
                
                cursor.execute(sql_sp, (id_usuario,))
                
                # Recuperamos los resultados
                filas = cursor.fetchall()

                if not filas:
                    print(f"\n[i] El usuario {id_usuario} no tiene canciones marcadas con 'Like'.")
                else:
                    print(f"\nCanciones favoritas del Usuario ID: {id_usuario}")
                    print("-" * 80)
                    # Formateo de cabecera
                    print(f"{'Canción':<25} | {'Artista':<20} | {'Álbum':<20} | {'Fecha Like'}")
                    print("-" * 80)
                    
                    for f in filas:
                        # f[0]=Cancion, f[1]=Artista, f[2]=Album, f[3]=Fecha
                        fecha = f[3].strftime('%Y-%m-%d %H:%M') if f[3] else "N/A"
                        print(f"{str(f[0]):<25} | {str(f[1]):<20} | {str(f[2]):<20} | {fecha}")
                    print("-" * 80)

            except Exception as e:
                # Aquí capturamos el RAISERROR del SP (si el usuario no existe)
                print(f"\n[X] Error del Sistema: {e}")
            finally:
                conn.close()

if __name__ == "__main__":
    # Asegúrate de que config.json esté en la misma carpeta
    db_conexion = ConexionBaseDatos('config.json')
    app = BibliotecaMusical(db_conexion)
    app.listar_canciones_like()