import json
import pyodbc
import os
from datetime import datetime
from model.Cancion import Cancion


# ============================================================
# GESTOR DE CANCIONES
# ============================================================
# Clase encargada de administrar todas las operaciones CRUD
# relacionadas con la tabla Catalogo.Cancion.
class GestorCancion:

    # ========================================================
    # CONSTRUCTOR DE LA CLASE
    # ========================================================
    # Inicializa la conexión con la base de datos SQL Server
    # utilizando los parámetros almacenados en config.json.
    def __init__(self):
        try:
            # Obtiene la ruta absoluta del directorio actual
            directorio = os.path.dirname(os.path.abspath(__file__))
            # Construye la ruta completa hacia el archivo config.json
            ruta = os.path.join(directorio, '..', 'config.json')
            # Abre y lee el archivo de configuración
            with open(ruta, 'r', encoding='utf-8') as archivo_config:
                config = json.load(archivo_config)
            # Obtiene los parámetros de conexión desde el archivo JSON
            controlador_odbc = config['controladorODBC']
            name_server = config['nameServer']
            database = config['database']
            username = config['username']
            password = config['password']
            # Construcción de la cadena de conexión
            self.connection_string = f"DRIVER={controlador_odbc};SERVER={name_server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;"
            # Establece conexión con la base de datos
            self.conn = pyodbc.connect(self.connection_string)
            print("Conexión exitosa a la base de datos.")
        # Manejo de error cuando no existe config.json
        except FileNotFoundError:
            print("[X] Error: No se encontró el archivo config.json.")
            self.conn = None
        # Manejo de error cuando faltan claves en el JSON
        except KeyError as e:
            print(f"[X] Error: Falta la clave {e} en el archivo config.json.")
            self.conn = None
        # Manejo de errores propios de SQL Server / pyodbc
        except pyodbc.Error as e:
            print(f"[X] Error de conexión a la base de datos: {e}")
            self.conn = None
        # Manejo de cualquier otro error inesperado
        except Exception as e:
            print(f"[X] Error inesperado: {e}")
            self.conn = None

    # ========================================================
    # MÉTODOS AUXILIARES DE VALIDACIÓN
    # ========================================================

    # Método para validar que un texto no esté vacío.
    def validar_texto_no_vacio(self, mensaje, mensaje_error):
        valor = ""
        # El bucle se repite hasta que el usuario ingrese un texto no vacío.
        while not valor.strip():
            valor = input(mensaje)
            # Si el texto ingresado es vacío, se muestra un mensaje de error y se solicita nuevamente.
            if not valor.strip():
                print(mensaje_error)
        return valor.strip()

    # Método para validar que un número entero sea mayor a cero.
    def validar_entero_mayor_a_cero(self, mensaje, mensaje_error):
        valor = 0
        # El bucle se repite hasta que el usuario ingrese un número entero válido y mayor a cero.
        while valor <= 0:
            try:
                valor = int(input(mensaje))
                # Si el número ingresado es menor o igual a cero, se muestra un mensaje de error.
                if valor <= 0:
                    print(mensaje_error)
                # Si el número es válido, se sale del bucle.
            except ValueError:
                print("Error: ingrese un número entero válido.")
        # Si el valor es válido, se devuelve.
        return valor

    # Método para validar que la opción ingresada por el usuario sea una de las opciones válidas.
    def validar_opcion(self, mensaje, opciones_validas, mensaje_error):
        valor = ""
        # El bucle se repite hasta que el usuario ingrese una opción válida.
        while valor not in opciones_validas:
            valor = input(mensaje).strip().lower()
            # Si la opción ingresada no es válida, se muestra un mensaje de error y se solicita nuevamente.
            if valor not in opciones_validas:
                print(mensaje_error)
        return valor

    # Método para validar que la calidad ingresada sea una de las opciones válidas (128, 192, 256, 320).
    def validar_calidad(self, mensaje):
        calidad = 0
        # El bucle se repite hasta que el usuario ingrese una calidad válida.
        while calidad not in (128, 192, 256, 320):
            try:
                calidad = int(input(mensaje))
                # Si la calidad ingresada no es válida, se muestra un mensaje de error.
                if calidad not in (128, 192, 256, 320):
                    print("Error: calidad no válida.")
                # Si la calidad es válida, se sale del bucle.
            except ValueError:
                print("Error: ingrese un número entero válido.")
        # Si la calidad es válida, se devuelve.
        return calidad

    # Método para validar el número de pista, que es un campo opcional.
    def validar_pista_opcional(self, mensaje):
        # El usuario puede ingresar un número de pista o dejarlo vacío.
        pista_raw = input(mensaje).strip()
        # Si el usuario ingresa un valor numérico, se convierte a entero; de lo contrario, se asigna None.
        pista = int(pista_raw) if pista_raw.isdigit() else None
        return pista

    # Método para validar que la fecha tenga el formato AAAA-MM-DD.
    def validar_fecha(self, mensaje):
        fecha = ""
        # El bucle se repite hasta que el usuario ingrese una fecha válida.
        while True:
            fecha = input(mensaje).strip()
            try:
                # Valida que la fecha exista y cumpla con el formato indicado.
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("Error: ingrese una fecha válida con el formato AAAA-MM-DD.")

    # ==============================================
    #               CREAR
    # ==============================================

    # Método encargado de insertar una nueva canción
    # en la base de datos mediante un procedimiento almacenado.
    def crear_cancion(self):
        # Encabezado visual
        print("\n" + "=" * 50)
        print("          INSERTAR CANCIÓN")
        print("=" * 50)
        # ====================================================
        # VALIDACIÓN DEL NOMBRE
        # ====================================================
        # El nombre no puede estar vacío.
        nombre = self.validar_texto_no_vacio(
            "Nombre de la canción: ",
            "Error: el nombre no puede estar vacío."
        )
        # ====================================================
        # VALIDACIÓN DE DURACIÓN
        # ====================================================
        # La duración debe ser un número entero mayor a 0.
        duracion = self.validar_entero_mayor_a_cero(
            "Duración en segundos: ",
            "Error: debe ser mayor a 0."
        )
        # Solicita la fecha de lanzamiento
        fecha = self.validar_fecha(
            "Fecha de lanzamiento (AAAA-MM-DD): "
        )
        # ====================================================
        # VALIDACIÓN DEL ESTADO
        # ====================================================
        # Solo se aceptan estados específicos.
        estado = self.validar_opcion(
            "Estado (activa/inactiva/bloqueada/eliminada): ",
            ('activa', 'inactiva', 'bloqueada', 'eliminada'),
            "Error: estado no válido."
        )
        # ====================================================
        # VALIDACIÓN DE CALIDAD
        # ====================================================
        # Solo se permiten ciertas calidades de audio.
        calidad = self.validar_calidad(
            "Calidad Kbps (128/192/256/320): "
        )
        # ====================================================
        # VALIDACIÓN DEL ID DEL ÁLBUM
        # ====================================================
        album_id = self.validar_entero_mayor_a_cero(
            "ID del álbum: ",
            "Error: el ID debe ser mayor a 0."
        )
        # ====================================================
        # NÚMERO DE PISTA
        # ====================================================
        # Campo opcional.
        # Si el valor ingresado es numérico se convierte a entero,
        # caso contrario se asigna None.
        pista = self.validar_pista_opcional(
            "Número de pista (Enter para omitir): "
        )

        cancion = Cancion(nombre, duracion, fecha, estado, calidad, album_id, pista)

        # Ejecuta el procedimiento almacenado
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_CrearCancion (?, ?, ?, ?, ?, ?, ?)}",
                (
                    cancion.nombre,
                    cancion.duracion,
                    cancion.fecha,
                    cancion.estado,
                    cancion.calidad,
                    cancion.album_id,
                    cancion.pista
                )
            )
            resultado = cursor.fetchone()
            self.conn.commit()

            # Verifica si se recibió respuesta
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
            if cursor:
                cursor.close()

    # ==============================================
    #               CONSULTAR
    # ==============================================

    # Método encargado de consultar canciones específicas
    # o listar todas las canciones registradas.
    def consultar_cancion(self):
        print("\n" + "=" * 50)
        print("          CONSULTAR CANCIONES")
        print("=" * 50)
        # Solicita el ID de canción
        # Si el usuario presiona Enter, se consultan todas.
        raw = input("ID de canción (Enter para ver todas): ").strip()
        # Si el valor ingresado es numérico se convierte a entero, caso contrario se asigna None.
        id_cancion = int(raw) if raw.isdigit() else None
        # Inicializa el cursor como None para luego cerrarlo correctamente en el bloque finally.
        cursor = None
        try:
            # Crea el cursor
            cursor = self.conn.cursor()
            # Ejecuta el procedimiento almacenado
            cursor.execute(
                "{CALL Catalogo.sp_ConsultarCancion (?)}",
                (id_cancion,)
            )
            # Obtiene todas las filas resultantes
            filas = cursor.fetchall()
            # Verifica si existen registros
            if not filas:
                print("\n[i] No se encontraron canciones.")
                return
            # Encabezado de la tabla
            print("\n" + "-" * 90)
            print(
                f"{'ID':<5} {'Nombre':<30} {'Dur(s)':>6} {'Estado':<12} "
                f"{'Kbps':>4} {'Reprod.':>8} {'Pista':>5} {'Álbum'}"
            )
            print("-" * 90)
            # Recorre cada fila obtenida
            for f in filas:
                # Si la pista es nula, se muestra "-"
                pista = str(f[7]) if f[7] else "-"
                # Imprime la información formateada
                print(
                    f"{f[0]:<5} {str(f[1]):<30} {f[2]:>6} {str(f[4]):<12} "
                    f"{f[5]:>4} {f[6]:>8} {pista:>5} {f[8]}"
                )
            print("-" * 90)
            # Muestra el total de registros encontrados
            print(f"Total de registros: {len(filas)}")
        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            if cursor:
                cursor.close()

    # =============================================================
    #               ACTUALIZAR
    # =============================================================
    # Método encargado de modificar los datos de una canción.
    def actualizar_cancion(self):
        print("\n" + "=" * 50)
        print("          ACTUALIZAR CANCIÓN")
        print("=" * 50)
        # Muestra las canciones registradas antes de actualizar
        self.consultar_cancion()
        # ====================================================
        # VALIDACIÓN DEL ID
        # ====================================================
        id_cancion = self.validar_entero_mayor_a_cero(
            "\nID de la canción a actualizar: ",
            "Error: el ID debe ser mayor a 0."
        )
        # Solicita el nuevo nombre
        nombre = self.validar_texto_no_vacio(
            "Nuevo nombre: ",
            "Error: el nombre no puede estar vacío."
        )
        # Solicita la nueva duración
        duracion = self.validar_entero_mayor_a_cero(
            "Nueva duración en segundos: ",
            "Error: debe ser mayor a 0."
        )
        # Solicita nueva fecha
        fecha = self.validar_fecha(
            "Nueva fecha de lanzamiento (AAAA-MM-DD): "
        )
        # Solicita nuevo estado
        estado = self.validar_opcion(
            "Nuevo estado (activa/inactiva/bloqueada/eliminada): ",
            ('activa', 'inactiva', 'bloqueada', 'eliminada'),
            "Error: estado no válido."
        )
        # Solicita nueva calidad
        calidad = self.validar_calidad(
            "Nueva calidad Kbps (128/192/256/320): "
        )
        # Campo opcional de pista
        pista = self.validar_pista_opcional(
            "Nuevo número de pista (Enter para omitir): "
        )

        cancion = Cancion(nombre, duracion, fecha, estado, calidad, None, pista)

        # Ejecuta el procedimiento almacenado de actualización
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_ActualizarCancion (?, ?, ?, ?, ?, ?, ?)}",
                (
                    id_cancion,
                    cancion.nombre,
                    cancion.duracion,
                    cancion.fecha,
                    cancion.estado,
                    cancion.calidad,
                    cancion.pista
                )
            )
            resultado = cursor.fetchone()
            self.conn.commit()

            # Verifica respuesta
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
            if cursor:
                cursor.close()

    # =============================================================
    #               ELIMINAR
    # =============================================================
    # Método encargado de eliminar una canción.
    def eliminar_cancion(self):
        print("\n" + "=" * 50)
        print("          ELIMINAR CANCIÓN")
        print("=" * 50)
        # Muestra canciones registradas antes de eliminar
        self.consultar_cancion()
        # Solicita el ID de la canción a eliminar
        id_cancion = self.validar_entero_mayor_a_cero(
            "\nID de la canción a eliminar: ",
            "Error: el ID debe ser mayor a 0."
        )
        # Ejecuta el procedimiento almacenado de eliminación
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "{CALL Catalogo.sp_EliminarCancion (?)}",
                (id_cancion,)
            )
            resultado = cursor.fetchone()
            self.conn.commit()

            # Verifica respuesta
            if resultado:

                print("\n" + "-" * 50)
                print(f"[OK] {resultado[0]}")
                print(f"     ID eliminado: {resultado[1]}")
                print("-" * 50)

        except Exception as e:
            print(f"\n[X] Error: {e}")
        finally:
            if cursor:
                cursor.close()
    
    # ============================================================
    #               MENÚ PRINCIPAL
    # ============================================================
    def ejecutar_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("        SISTEMA CRUD - CATÁLOGO CANCIONES   ")
            print("=" * 50)
            print("\t1. Insertar canción")
            print("\t2. Consultar canciones")
            print("\t3. Actualizar canción")
            print("\t4. Eliminar canción")
            print("\t5. Salir")
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
                print("\n[!] Opción no válida. Intente nuevamente.")

    # ============================================================
    #               CERRAR CONEXIÓN
    # ============================================================
    # Método encargado de cerrar correctamente la conexión
    # con la base de datos.
    def cerrar_conexion(self):
        # Verifica si existe una conexión activa
        if self.conn:
            # Cierra la conexión
            self.conn.close()
            print("Conexión cerrada correctamente.")