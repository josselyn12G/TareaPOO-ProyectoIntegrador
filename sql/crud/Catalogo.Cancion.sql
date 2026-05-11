CREATE TABLE Catalogo.Cancion (
    idCancion          INT           IDENTITY(1,1)  NOT NULL,
    nombreCancion      NVARCHAR(150)                NOT NULL,
    duracion           INT                          NOT NULL,  -- duración en segundos
    fechaLanzamiento   DATE                         NOT NULL,
    estadoCancion      NVARCHAR(20)                 NOT NULL,  -- ej: 'activa', 'inactiva'
    calidadKbps        INT                          NOT NULL,  -- ej: 128, 192, 320
    Album_idAlbum      INT                          NOT NULL,
    numeroPista        INT                          NOT NULL,

    CONSTRAINT PK_Cancion        PRIMARY KEY (idCancion),
    CONSTRAINT FK_Cancion_Album  FOREIGN KEY (Album_idAlbum)
                                 REFERENCES Catalogo.Album (idAlbum),
    CONSTRAINT CK_Calidad        CHECK (calidadKbps IN (128, 192, 256, 320)),
    CONSTRAINT CK_Estado         CHECK (estadoCancion IN ('activa', 'inactiva')),
    CONSTRAINT CK_Duracion       CHECK (duracion > 0),
    CONSTRAINT CK_NumeroPista    CHECK (numeroPista > 0)
);