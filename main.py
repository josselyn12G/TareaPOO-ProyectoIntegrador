from gestor_cancion import GestorCancion


# ============================================================
# FUNCIÓN PRINCIPAL DEL MENÚ
# ============================================================
def ejecutar_menu():

    # Crear una instancia de la clase GestorCancion
    # Esta clase contiene los métodos CRUD y la conexión
    # con la base de datos.
    gestor = GestorCancion()

    # Verificar si la conexión a la base de datos fue exitosa
    if gestor.conn is None:
        print("No se puede iniciar el sistema porque no existe conexión a la base de datos.")
        return

    # Bucle principal del sistema
    # Se ejecuta hasta que el usuario seleccione la opción de salir.
    while True:

        # Mostrar el menú de opciones
        print("\n" + "=" * 50)
        print("      SISTEMA CRUD - CATALOGO.CANCION")
        print("=" * 50)
        print("  1. Crear canción")
        print("  2. Consultar canciones")
        print("  3. Actualizar canción")
        print("  4. Eliminar canción")
        print("  5. Salir")
        print("=" * 50)

        # Solicitar al usuario una opción del menú
        opcion = input("Seleccione una opción (1-5): ").strip()

        # ====================================================
        # OPCIÓN 1 - CREAR CANCIÓN
        # ====================================================
        if opcion == "1":
            gestor.crear_cancion()

        # ====================================================
        # OPCIÓN 2 - CONSULTAR CANCIONES
        # ====================================================
        elif opcion == "2":
            gestor.consultar_cancion()

        # ====================================================
        # OPCIÓN 3 - ACTUALIZAR CANCIÓN
        # ====================================================
        elif opcion == "3":
            gestor.actualizar_cancion()

        # ====================================================
        # OPCIÓN 4 - ELIMINAR CANCIÓN
        # ====================================================
        elif opcion == "4":
            gestor.eliminar_cancion()

        # ====================================================
        # OPCIÓN 5 - SALIR DEL SISTEMA
        # ====================================================
        elif opcion == "5":
            print("\nSaliendo del sistema...")

            # Cerrar la conexión con la base de datos
            gestor.cerrar_conexion()
            break

        # ====================================================
        # OPCIÓN INVÁLIDA
        # ====================================================
        else:
            print("\n[!] Opción no válida. Intente de nuevo.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================
# Esta condición verifica si el archivo se está ejecutando
# directamente y no siendo importado desde otro módulo.
if __name__ == "__main__":
    ejecutar_menu()