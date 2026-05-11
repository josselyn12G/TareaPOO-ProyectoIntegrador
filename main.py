from crud.GestorCancion import GestorCancion


if __name__ == "__main__":
    gestor = GestorCancion()
    if gestor.conn:
        gestor.ejecutar_menu()
        gestor.cerrar_conexion()