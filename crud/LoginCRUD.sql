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
-- Verificar que todo quedó bien
-- ============================================================
SELECT 
    r.name  AS Rol,
    m.name  AS Usuario
FROM sys.database_role_members  rm
JOIN sys.database_principals    r ON rm.role_principal_id   = r.principal_id
JOIN sys.database_principals    m ON rm.member_principal_id = m.principal_id
WHERE r.name = 'RolCrudCancion';
GO