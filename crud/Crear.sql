USE Ecualizer;
GO

-- ============================================================
-- SP: Catalogo.sp_CrearCancion
-- Descripción: Inserta una nueva canción en Catalogo.Cancion.
-- Validaciones:
--   - El álbum debe existir
--   - El estado debe ser: activa, inactiva, bloqueada o eliminada
--   - La duración debe ser mayor a 0
--   - La calidad debe ser: 128, 192, 256 o 320
-- Manejo de errores: RAISERROR + ROLLBACK TRANSACTION
-- ============================================================

CREATE OR ALTER PROCEDURE Catalogo.sp_CrearCancion
    @nombreCancion  VARCHAR(150),
    @duracion       SMALLINT,
    @fechaLanz      DATE,
    @estado         VARCHAR(20),
    @calidad        SMALLINT,
    @Album_idAlbum  INT,
    @numeroPista    SMALLINT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Validación: el álbum debe existir
    IF NOT EXISTS (SELECT 1 FROM Catalogo.Album WHERE idAlbum = @Album_idAlbum)
    BEGIN
        RAISERROR('Error: El álbum especificado no existe.', 16, 1);
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

        INSERT INTO Catalogo.Cancion
            (nombreCancion, duracion, fechaLanzamiento,
             estadoCancion, calidadKbps, Album_idAlbum, numeroPista)
        VALUES
            (@nombreCancion, @duracion, @fechaLanz,
             @estado, @calidad, @Album_idAlbum, @numeroPista);

        DECLARE @nuevoId INT = SCOPE_IDENTITY();

        COMMIT TRANSACTION;

        SELECT
            'Canción insertada correctamente' AS Mensaje,
            @nuevoId                          AS NuevoID,
            @nombreCancion                    AS Nombre,
            @duracion                         AS Duracion,
            @estado                           AS Estado;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- ============================================================
-- PRUEBA 1: Inserción exitosa
-- ============================================================
EXEC Catalogo.sp_CrearCancion
    @nombreCancion = 'Cancion de prueba Anthony',
    @duracion      = 200,
    @fechaLanz     = '2024-01-01',
    @estado        = 'activa',
    @calidad       = 320,
    @Album_idAlbum = 1,
    @numeroPista   = 6;
GO

-- ============================================================
-- PRUEBA 2: Error - álbum inexistente
-- ============================================================
EXEC Catalogo.sp_CrearCancion
    @nombreCancion = 'Cancion invalida',
    @duracion      = 180,
    @fechaLanz     = '2024-01-01',
    @estado        = 'activa',
    @calidad       = 320,
    @Album_idAlbum = 999;
GO

-- ============================================================
-- PRUEBA 3: Error - estado no válido
-- ============================================================
EXEC Catalogo.sp_CrearCancion
    @nombreCancion = 'Cancion invalida',
    @duracion      = 180,
    @fechaLanz     = '2024-01-01',
    @estado        = 'suspendida',
    @calidad       = 320,
    @Album_idAlbum = 1;
GO