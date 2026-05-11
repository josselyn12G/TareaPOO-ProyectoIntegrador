USE master;
GO

-- ============================================================
-- Crear Login
-- ============================================================
CREATE LOGIN login_CrudCancion
    WITH PASSWORD = 'Crud@Cancion2026!',
    CHECK_POLICY = ON,
    CHECK_EXPIRATION = OFF;
GO

-- ============================================================
-- Crear Usuario en Ecualizer
-- ============================================================
USE Ecualizer;
GO

CREATE USER user_CrudCancion
    FOR LOGIN login_CrudCancion
    WITH DEFAULT_SCHEMA = Catalogo;
GO

-- ============================================================
-- Crear Rol
-- ============================================================
CREATE ROLE RolCrudCancion;
GO

-- ============================================================
-- Dar permisos al Rol
-- ============================================================
GRANT EXECUTE ON Catalogo.sp_CrearCancion      TO RolCrudCancion;
GRANT EXECUTE ON Catalogo.sp_ConsultarCancion  TO RolCrudCancion;
GRANT EXECUTE ON Catalogo.sp_ActualizarCancion TO RolCrudCancion;
GRANT EXECUTE ON Catalogo.sp_EliminarCancion   TO RolCrudCancion;
GO

-- ============================================================
-- Asignar usuario al Rol
-- ============================================================
ALTER ROLE RolCrudCancion ADD MEMBER user_CrudCancion;
GO


-- ============================================================
-- Cambiar contexto al usuario
-- ============================================================
EXECUTE AS USER = 'user_CrudCancion';
GO

-- ============================================================
-- Validar consulta de canciones
-- ============================================================
EXEC Catalogo.sp_ConsultarCancion;
GO

-- ============================================================
-- Validar creación de canción
-- ============================================================
EXEC Catalogo.sp_CrearCancion
    @Titulo = 'Cancion Demo',
    @Duracion = '03:45',
    @GeneroID = 1,
    @ArtistaID = 1;
GO

-- ============================================================
-- Validar actualización de canción
-- ============================================================
EXEC Catalogo.sp_ActualizarCancion
    @CancionID = 1,
    @Titulo = 'Cancion Actualizada',
    @Duracion = '04:00',
    @GeneroID = 1,
    @ArtistaID = 1;
GO

-- ============================================================
-- Validar eliminación de canción
-- ============================================================
EXEC Catalogo.sp_EliminarCancion
    @CancionID = 1;
GO