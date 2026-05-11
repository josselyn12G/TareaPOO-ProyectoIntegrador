USE Ecualizer
GO

-- ============================================================
-- ESQUEMA: Catalogo
-- Descripción:
-- Las tablas Album y Cancion fueron recuperadas y adaptadas
-- de nuestro proyecto desarrollado previamente para la gestión
-- de contenido musical dentro de la plataforma Ecualizer.
-- ============================================================

CREATE SCHEMA Catalogo
GO

-- ============================================================
-- TABLA: Album
-- Descripción:
-- Almacena la información principal de los álbumes musicales.
-- ============================================================

CREATE TABLE Catalogo.Album (
    idAlbum            INT            IDENTITY(1,1) NOT NULL,
    tituloAlbum        NVARCHAR(150)                NOT NULL,
    artista            NVARCHAR(150)                NOT NULL,
    fechaLanzamiento   DATE                         NOT NULL,
    genero             NVARCHAR(100)                NOT NULL,
    estadoAlbum        NVARCHAR(20)                 NOT NULL, -- ej: 'activo', 'inactivo'

    CONSTRAINT PK_Album
        PRIMARY KEY (idAlbum),

    CONSTRAINT CK_EstadoAlbum
        CHECK (estadoAlbum IN ('activo', 'inactivo'))
);
GO

-- ============================================================
-- TABLA: Cancion
-- Descripción:
-- Almacena las canciones pertenecientes a un álbum musical.
-- ============================================================

CREATE TABLE Catalogo.Cancion (
    idCancion             INT            IDENTITY(1,1) NOT NULL,
    nombreCancion         NVARCHAR(150)                 NOT NULL,
    duracion              INT                           NOT NULL, -- duración en segundos
    fechaLanzamiento      DATE                          NOT NULL,
    estadoCancion         NVARCHAR(20)                  NOT NULL, -- ej: 'activa', 'inactiva'
    calidadKbps           INT                           NOT NULL, -- ej: 128, 192, 256, 320
    totalReproducciones   INT                           NOT NULL DEFAULT 0,
    Album_idAlbum         INT                           NOT NULL,
    numeroPista           INT                           NULL,

    CONSTRAINT PK_Cancion
        PRIMARY KEY (idCancion),

    CONSTRAINT FK_Cancion_Album
        FOREIGN KEY (Album_idAlbum)
        REFERENCES Catalogo.Album (idAlbum),

    CONSTRAINT CK_Calidad
        CHECK (calidadKbps IN (128, 192, 256, 320)),

    CONSTRAINT CK_Estado
        CHECK (estadoCancion IN ('activa', 'inactiva')),

    CONSTRAINT CK_Duracion
        CHECK (duracion > 0),

    CONSTRAINT CK_NumeroPista
        CHECK (numeroPista IS NULL OR numeroPista > 0),

    CONSTRAINT CK_TotalReproducciones
        CHECK (totalReproducciones >= 0)
);
GO

-- ============================================================
-- INSERCIÓN DE ÁLBUMES
-- Descripción:
-- Inserta registros de ejemplo en la tabla Album.
-- ============================================================

INSERT INTO Catalogo.Album (
    tituloAlbum,
    artista,
    fechaLanzamiento,
    genero,
    estadoAlbum
)
VALUES
(
    'Random Access Memories',
    'Daft Punk',
    '2013-05-17',
    'Electronic',
    'activo'
),
(
    'After Hours',
    'The Weeknd',
    '2020-03-20',
    'R&B',
    'activo'
),
(
    'Back in Black',
    'AC/DC',
    '1980-07-25',
    'Rock',
    'activo'
);
GO

