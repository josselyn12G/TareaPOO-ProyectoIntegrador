USE Ecualizer;
GO

-- ============================================================
-- SP: Catalogo.sp_EliminarCancion
-- Descripción: Elimina una canción de Catalogo.Cancion.
--              Primero limpia registros relacionados en
--              CancionGeneroMusical y CancionPlaylist.
-- Validaciones:
--   - La canción debe existir
--   - No puede eliminarse si tiene reproducciones registradas
--     (integridad referencial con Analitica.Reproduccion)
-- Manejo de errores: RAISERROR + ROLLBACK TRANSACTION
-- ============================================================

CREATE OR ALTER PROCEDURE Catalogo.sp_EliminarCancion
    @idCancion INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Validación: la canción debe existir
    IF NOT EXISTS (SELECT 1 FROM Catalogo.Cancion WHERE idCancion = @idCancion)
    BEGIN
        RAISERROR('Error: No existe una canción con el ID %d.', 16, 1, @idCancion);
        RETURN;
    END

    -- Validación: no puede tener reproducciones registradas
    IF EXISTS (
        SELECT 1 FROM Analitica.Reproduccion
        WHERE Cancion_idCancion = @idCancion
    )
    BEGIN
        RAISERROR('Error: No se puede eliminar la canción porque tiene reproducciones registradas. Debe eliminar primero los registros dependientes.', 16, 1);
        RETURN;
    END

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Limpiar géneros asociados
        DELETE FROM Catalogo.CancionGeneroMusical
        WHERE Cancion_idCancion = @idCancion;

        -- Limpiar canciones en playlists
        DELETE FROM Biblioteca.CancionPlaylist
        WHERE Cancion_idCancion = @idCancion;

        -- Limpiar likes
        DELETE FROM Biblioteca.UsuarioCancionLike
        WHERE Cancion_idCancion = @idCancion;

        -- Eliminar la canción
        DELETE FROM Catalogo.Cancion
        WHERE idCancion = @idCancion;

        COMMIT TRANSACTION;

        SELECT
            'Canción eliminada correctamente' AS Mensaje,
            @idCancion                        AS IDEliminado;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- ============================================================
-- PRUEBA 1: Primero insertar una canción para luego eliminarla
-- ============================================================
EXEC Catalogo.sp_CrearCancion
    @nombreCancion = 'Cancion para eliminar',
    @duracion      = 150,
    @fechaLanz     = '2024-06-01',
    @estado        = 'activa',
    @calidad       = 128,
    @Album_idAlbum = 1;
GO

-- Consulta para ver el ID generado
SELECT TOP 1 idCancion, nombreCancion
FROM Catalogo.Cancion
ORDER BY idCancion DESC;
GO

-- ============================================================
-- PRUEBA 2: Eliminar la canción recién creada

-- ============================================================
EXEC Catalogo.sp_EliminarCancion @idCancion = 1004;
GO

-- ============================================================
-- PRUEBA 3: Error - canción inexistente
-- ============================================================
EXEC Catalogo.sp_EliminarCancion @idCancion = 999;
GO

-- ============================================================
-- PRUEBA 4: Error - canción con reproducciones (ID 21 tiene)
-- ============================================================
EXEC Catalogo.sp_EliminarCancion @idCancion = 21;
GO