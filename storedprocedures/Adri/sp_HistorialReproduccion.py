import json
import pyodbc
import os

class ConexionBaseDatos:
    def __init__(self, nombre_archivo):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
        self.datos_conexion = self._leer_config()

    def _leer_config(self):
        try:
            if not os.path.exists(self.ruta_archivo):
                print(f"\n[!] ERROR: No se encontró {self.ruta_archivo}")
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

class AnaliticaUsuario:
    def __init__(self, db):
        self.db = db

    def consultar_historial(self):
        print("\n--- HISTORIAL DE REPRODUCCIÓN ---")
        
        # Parámetro obligatorio
        id_usuario = input("ID del Usuario a consultar *: ")
        
        # Parámetros opcionales (pueden quedar vacíos)
        print("(Opcional: Presione Enter para omitir fechas)")
        f_inicio = input("Fecha Inicio (AAAA-MM-DD): ").strip() or None
        f_fin = input("Fecha Fin (AAAA-MM-DD): ").strip() or None

        conn = self.db.obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Invocamos el SP con 3 parámetros
                # SQL Server acepta NULL si no mandamos valor en los opcionales
                sql_sp = "{CALL Analitica.sp_HistorialReproduccionUsuario (?, ?, ?)}"
                
                cursor.execute(sql_sp, (id_usuario, f_inicio, f_fin))
                
                filas = cursor.fetchall()

                if not filas:
                    print(f"\n[i] No se encontró actividad para el usuario {id_usuario} en ese rango.")
                else:
                    print(f"\nActividad del Usuario ID: {id_usuario}")
                    print("-" * 100)
                    print(f"{'Título':<25} | {'Artista':<20} | {'Fecha':<12} | {'Hora':<10} | {'Duración (s)'}")
                    print("-" * 100)
                    
                    for f in filas:
                        # f[0]=Titulo, f[1]=Artista, f[2]=Album (omitido aquí), f[3]=Fecha, f[4]=Hora, f[5]=Duracion
                        print(f"{str(f[0]):<25} | {str(f[1]):<20} | {str(f[3]):<12} | {str(f[4]):<10} | {f[5]}")
                    print("-" * 100)

            except Exception as e:
                # Captura errores de validación como 'Usuario no encontrado'
                print(f"\n[X] Error del Procedimiento: {e}")
            finally:
                conn.close()

if __name__ == "__main__":
    app = AnaliticaUsuario(ConexionBaseDatos('config.json'))
    app.consultar_historial()