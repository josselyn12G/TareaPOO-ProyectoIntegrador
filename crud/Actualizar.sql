USE Ecualizer;
GO

-- ============================================================
-- SP: Catalogo.sp_ActualizarCancion
-- Descripción: Actualiza los datos de una canción existente.
-- Validaciones:
--   - La canción debe existir
--   - El estado debe ser válido
--   - La duración debe ser mayor a 0
--   - La calidad debe ser: 128, 192, 256 o 320
-- Manejo de errores: RAISERROR + ROLLBACK TRANSACTION
-- ============================================================

CREATE OR ALTER PROCEDURE Catalogo.sp_ActualizarCancion
    @idCancion      INT,
    @nombreCancion  VARCHAR(150),
    @duracion       SMALLINT,
    @fechaLanz      DATE,
    @estado         VARCHAR(20),
    @calidad        SMALLINT,
    @numeroPista    SMALLINT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Validación: la canción debe existir
    IF NOT EXISTS (SELECT 1 FROM Catalogo.Cancion WHERE idCancion = @idCancion)
    BEGIN
        RAISERROR('Error: No existe una canción con el ID %d.', 16, 1, @idCancion);
        RETURN;
    END

    -- Validación: estado válido
    IF @estado NOT IN ('activa', 'inactiva', 'bloqueada', 'eliminada')
    BEGIN
        RAISERROR('Error: Estado no válido. Use: activa, inactiva, bloqueada o eliminada.', 16, 1);
        RETURN;
    END

    -- Validación: duración mayor a 0
    IF @duracion <= 0
    BEGIN
        RAISERROR('Error: La duración debe ser mayor a 0.', 16, 1);
        RETURN;
    END

    -- Validación: calidad permitida
    IF @calidad NOT IN (128, 192, 256, 320)
    BEGIN
        RAISERROR('Error: Calidad no válida. Use: 128, 192, 256 o 320.', 16, 1);
        RETURN;
    END

    BEGIN TRY
        BEGIN TRANSACTION;

        UPDATE Catalogo.Cancion
        SET
            nombreCancion    = @nombreCancion,
            duracion         = @duracion,
            fechaLanzamiento = @fechaLanz,
            estadoCancion    = @estado,
            calidadKbps      = @calidad,
            numeroPista      = @numeroPista
        WHERE idCancion = @idCancion;

        COMMIT TRANSACTION;

        SELECT
            'Canción actualizada correctamente' AS Mensaje,
            @idCancion                          AS ID,
            @nombreCancion                      AS NuevoNombre,
            @estado                             AS NuevoEstado;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- ============================================================
-- PRUEBA 1: Actualización exitosa
-- ============================================================
EXEC Catalogo.sp_ActualizarCancion
    @idCancion     = 1,
    @nombreCancion = 'Rockstar Edicion Especial',
    @duracion      = 210,
    @fechaLanz     = '2018-09-21',
    @estado        = 'activa',
    @calidad       = 320,
    @numeroPista   = 1;
GO

-- ============================================================
-- PRUEBA 2: Error - canción inexistente
-- ============================================================
EXEC Catalogo.sp_ActualizarCancion
    @idCancion     = 999,
    @nombreCancion = 'No existe',
    @duracion      = 200,
    @fechaLanz     = '2024-01-01',
    @estado        = 'activa',
    @calidad       = 320;
GO

-- ============================================================
-- PRUEBA 3: Error - duración inválida
-- ============================================================
EXEC Catalogo.sp_ActualizarCancion
    @idCancion     = 1,
    @nombreCancion = 'Rockstar',
    @duracion      = -5,
    @fechaLanz     = '2018-09-21',
    @estado        = 'activa',
    @calidad       = 320;
GO