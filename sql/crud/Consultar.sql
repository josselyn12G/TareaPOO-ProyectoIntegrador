USE Ecualizer;
GO

-- ============================================================
-- SP: Catalogo.sp_ConsultarCancion
-- Descripción: Consulta una canción por ID o todas las canciones.
--              Incluye el nombre del álbum al que pertenece.
-- Validaciones:
--   - Si se proporciona un ID, debe existir en la tabla
-- Manejo de errores: RAISERROR si el ID no existe
-- ============================================================

CREATE OR ALTER PROCEDURE Catalogo.sp_ConsultarCancion
    @idCancion INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Validación: si se da un ID, debe existir
    IF @idCancion IS NOT NULL AND
       NOT EXISTS (SELECT 1 FROM Catalogo.Cancion WHERE idCancion = @idCancion)
    BEGIN
        RAISERROR('Error: No existe una canción con ese ID.', 16, 1);
        RETURN;
    END

    SELECT
        C.idCancion,
        C.nombreCancion,
        C.duracion,
        C.fechaLanzamiento,
        C.estadoCancion,
        C.calidadKbps,
        C.totalReproducciones,
        C.numeroPista,
        AL.tituloAlbum
    FROM Catalogo.Cancion C
    INNER JOIN Catalogo.Album AL ON C.Album_idAlbum = AL.idAlbum
    WHERE (@idCancion IS NULL OR C.idCancion = @idCancion)
    ORDER BY C.idCancion;
END;
GO

-- ============================================================
-- PRUEBA 1: Consultar todas las canciones
-- ============================================================
EXEC Catalogo.sp_ConsultarCancion;
GO

-- ============================================================
-- PRUEBA 2: Consultar canción específica
-- ============================================================
EXEC Catalogo.sp_ConsultarCancion @idCancion = 1;
GO

-- ============================================================
-- PRUEBA 3: Error - ID inexistente
-- ============================================================
EXEC Catalogo.sp_ConsultarCancion @idCancion = 999;
GO