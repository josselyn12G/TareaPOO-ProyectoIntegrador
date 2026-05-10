import json
import pyodbc
import os

# ============================================================
# CONEXIÓN
# ============================================================
class ConexionBDD:
    def __init__(self):
        directorio = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(directorio, 'config.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            config = json.load(f)
        cadena = (
            f"DRIVER={config['controladorODBC']};"
            f"SERVER={config['nameServer']};"
            f"DATABASE={config['database']};"
            f"UID={config['username']};"
            f"PWD={config['password']};"
            f"TrustServerCertificate=yes;"
        )
        self.conexion = pyodbc.connect(cadena)
        print("Conexión exitosa a la base de datos.")

# ============================================================
# GESTOR DE CANCIONES
# ============================================================
class GestorCancion:
    def __init__(self, db: ConexionBDD):
        self.conn = db.conexion

    # ─── CREAR ───────────────────────────────────────────────
    def crear_cancion(self):
        print("\n" + "=" * 50)
        print("          INSERTAR CANCIÓN")
        print("=" * 50)

        nombre = ""
        while not nombre.strip():
            nombre = input("Nombre de la canción: ")
            if not nombre.strip():
                print("Error: el nombre no puede estar vacío.")

        duracion = 0
        while duracion <= 0:
            try:
                duracion = int(input("Duración en segundos: "))
                if duracion <= 0:
                    print("Error: debe ser mayor a 0.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        fecha = input("Fecha de lanzamiento (AAAA-MM-DD): ").strip()

        estado = ""
        while estado not in ('activa', 'inactiva', 'bloqueada', 'eliminada'):
            estado = input("Estado (activa/inactiva/bloqueada/eliminada): ").strip().lower()
            if estado not in ('activa', 'inactiva', 'bloqueada', 'eliminada'):
                print("Error: estado no válido.")

        calidad = 0
        while calidad not in (128, 192, 256, 320):
            try:
                calidad = int(input("Calidad Kbps (128/192/256/320): "))
                if calidad not in (128, 192, 256, 320):
                    print("Error: calidad no válida.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        album_id = 0
        while album_id <= 0:
            try:
                album_id = int(input("ID del álbum: "))
                if album_id <= 0:
                    print("Error: el ID debe ser mayor a 0.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        pista_raw = input("Número de pista (Enter para omitir): ").strip()
        pista = int(pista_raw) if pista_raw.isdigit() else None

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_CrearCancion (?, ?, ?, ?, ?, ?, ?)}",
                (nombre, duracion, fecha, estado, calidad, album_id, pista)
            )
            resultado = cursor.fetchone()
            self.conn.commit()
            if resultado:
                print("\n" + "-" * 50)
                print(f"[OK] {resultado[0]}")
                print(f"     ID generado : {resultado[1]}")
                print(f"     Nombre      : {resultado[2]}")
                print(f"     Duración    : {resultado[3]}s")
                print(f"     Estado      : {resultado[4]}")
                print("-" * 50)
        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            cursor.close()

    # ─── CONSULTAR ───────────────────────────────────────────
    def consultar_cancion(self):
        print("\n" + "=" * 50)
        print("          CONSULTAR CANCIONES")
        print("=" * 50)

        raw = input("ID de canción (Enter para ver todas): ").strip()
        id_cancion = int(raw) if raw.isdigit() else None

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_ConsultarCancion (?)}",
                (id_cancion,)
            )
            filas = cursor.fetchall()

            if not filas:
                print("\n[i] No se encontraron canciones.")
                return

            # Encabezado de la tabla
            print("\n" + "-" * 90)
            print(f"{'ID':<5} {'Nombre':<30} {'Dur(s)':>6} {'Estado':<12} "
                  f"{'Kbps':>4} {'Reprod.':>8} {'Pista':>5} {'Álbum'}")
            print("-" * 90)

            # Filas de la tabla
            for f in filas:
                pista = str(f[7]) if f[7] else "-"
                print(f"{f[0]:<5} {str(f[1]):<30} {f[2]:>6} {str(f[4]):<12} "
                      f"{f[5]:>4} {f[6]:>8} {pista:>5} {f[8]}")

            print("-" * 90)
            print(f"Total de registros: {len(filas)}")

        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            cursor.close()

    # ─── ACTUALIZAR ──────────────────────────────────────────
    def actualizar_cancion(self):
        print("\n" + "=" * 50)
        print("          ACTUALIZAR CANCIÓN")
        print("=" * 50)

        # Mostrar canciones disponibles primero
        self.consultar_cancion()

        id_cancion = 0
        while id_cancion <= 0:
            try:
                id_cancion = int(input("\nID de la canción a actualizar: "))
                if id_cancion <= 0:
                    print("Error: el ID debe ser mayor a 0.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        nombre = ""
        while not nombre.strip():
            nombre = input("Nuevo nombre: ")
            if not nombre.strip():
                print("Error: el nombre no puede estar vacío.")

        duracion = 0
        while duracion <= 0:
            try:
                duracion = int(input("Nueva duración en segundos: "))
                if duracion <= 0:
                    print("Error: debe ser mayor a 0.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        fecha = input("Nueva fecha de lanzamiento (AAAA-MM-DD): ").strip()

        estado = ""
        while estado not in ('activa', 'inactiva', 'bloqueada', 'eliminada'):
            estado = input("Nuevo estado (activa/inactiva/bloqueada/eliminada): ").strip().lower()
            if estado not in ('activa', 'inactiva', 'bloqueada', 'eliminada'):
                print("Error: estado no válido.")

        calidad = 0
        while calidad not in (128, 192, 256, 320):
            try:
                calidad = int(input("Nueva calidad Kbps (128/192/256/320): "))
                if calidad not in (128, 192, 256, 320):
                    print("Error: calidad no válida.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        pista_raw = input("Nuevo número de pista (Enter para omitir): ").strip()
        pista = int(pista_raw) if pista_raw.isdigit() else None

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_ActualizarCancion (?, ?, ?, ?, ?, ?, ?)}",
                (id_cancion, nombre, duracion, fecha, estado, calidad, pista)
            )
            resultado = cursor.fetchone()
            self.conn.commit()
            if resultado:
                print("\n" + "-" * 50)
                print(f"[OK] {resultado[0]}")
                print(f"     ID          : {resultado[1]}")
                print(f"     Nuevo nombre: {resultado[2]}")
                print(f"     Nuevo estado: {resultado[3]}")
                print("-" * 50)
        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            cursor.close()

    # ─── ELIMINAR ────────────────────────────────────────────
    def eliminar_cancion(self):
        print("\n" + "=" * 50)
        print("          ELIMINAR CANCIÓN")
        print("=" * 50)

        # Mostrar canciones disponibles primero
        self.consultar_cancion()

        id_cancion = 0
        while id_cancion <= 0:
            try:
                id_cancion = int(input("\nID de la canción a eliminar: "))
                if id_cancion <= 0:
                    print("Error: el ID debe ser mayor a 0.")
            except ValueError:
                print("Error: ingrese un número entero válido.")

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_EliminarCancion (?)}",
                (id_cancion,)
            )
            resultado = cursor.fetchone()
            self.conn.commit()
            if resultado:
                print("\n" + "-" * 50)
                print(f"[OK] {resultado[0]}")
                print(f"     ID eliminado: {resultado[1]}")
                print("-" * 50)
        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            cursor.close()

    # ─── MENÚ PRINCIPAL ──────────────────────────────────────
    def ejecutar_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("      SISTEMA CRUD - CATALOGO.CANCION")
            print("=" * 50)
            print("  1. Crear canción")
            print("  2. Consultar canciones")
            print("  3. Actualizar canción")
            print("  4. Eliminar canción")
            print("  5. Salir")
            print("=" * 50)

            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                self.crear_cancion()
            elif opcion == "2":
                self.consultar_cancion()
            elif opcion == "3":
                self.actualizar_cancion()
            elif opcion == "4":
                self.eliminar_cancion()
            elif opcion == "5":
                print("\nSaliendo del sistema...")
                break
            else:
                print("\n[!] Opción no válida. Intente de nuevo.")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    db = ConexionBDD()
    gestor = GestorCancion(db)
    gestor.ejecutar_menu()