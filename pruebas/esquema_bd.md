CREATE TABLE marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre_marca TEXT
);
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria TEXT
);
CREATE TABLE subcategorias (
    id_subcategoria SERIAL PRIMARY KEY,
    nombre_subcategoria TEXT
);
CREATE TABLE formatos (
    id_formato SERIAL PRIMARY KEY,
    nombre_formato TEXT
);
CREATE TABLE responsabilidades (
    id_responsabilidad SERIAL PRIMARY KEY,
    nombre_responsabilidad TEXT
);
CREATE TABLE sombras (
    id_efecto_sombra SERIAL PRIMARY KEY,
    nombre_efecto_sombra TEXT
);
CREATE TABLE labios (
    id_efecto_labios SERIAL PRIMARY KEY,
    nombre_efecto_labios TEXT
);
CREATE TABLE mascaras (
    id_efecto_mascara SERIAL PRIMARY KEY,
    nombre_efecto_mascara TEXT
);
CREATE TABLE brochas (
    id_tipo_brocha SERIAL PRIMARY KEY,
    nombre_tipo_brocha TEXT
);
CREATE TABLE formulaciones (
    id_formulacion SERIAL PRIMARY KEY,
    nombre_formulacion TEXT
);
CREATE TABLE pieles (
    id_tipo_piel SERIAL PRIMARY KEY,
    nombre_tipo_piel TEXT
);
CREATE TABLE coberturas (
    id_cobertura SERIAL PRIMARY KEY,
    nombre_cobertura TEXT
);
CREATE TABLE acabados (
    id_acabado SERIAL PRIMARY KEY,
    nombre_acabado TEXT
);
CREATE TABLE texturas (
    id_textura SERIAL PRIMARY KEY,
    nombre_textura TEXT
);
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto TEXT,
    descripcion_producto TEXT,
    precio FLOAT CHECK (precio >= 0),
    num_valoraciones INT,
    valoracion FLOAT CHECK (valoracion BETWEEN 0 AND 5),
    num_variaciones INT,
    id_marca INT REFERENCES marcas(id_marca) ON DELETE CASCADE,
    id_categoria INT REFERENCES categorias(id_categoria) ON DELETE CASCADE,
    id_subcategoria INT REFERENCES subcategorias(id_subcategoria) ON DELETE CASCADE,
    id_formato INT REFERENCES formatos(id_formato) ON DELETE CASCADE,
    id_responsabilidad INT REFERENCES responsabilidades(id_responsabilidad) ON DELETE CASCADE,
    id_efecto_sombra INT REFERENCES sombras(id_efecto_sombra) ON DELETE CASCADE,
    id_efecto_labios INT REFERENCES labios(id_efecto_labios) ON DELETE CASCADE,
    id_efecto_mascara INT REFERENCES mascaras(id_efecto_mascara) ON DELETE CASCADE,
    id_tipo_brocha INT REFERENCES brochas(id_tipo_brocha) ON DELETE CASCADE,
    id_formulacion INT REFERENCES formulaciones(id_formulacion) ON DELETE CASCADE,
    id_tipo_piel INT REFERENCES pieles(id_tipo_piel) ON DELETE CASCADE,
    id_cobertura INT REFERENCES coberturas(id_cobertura) ON DELETE CASCADE,
    id_acabado INT REFERENCES acabados(id_acabado) ON DELETE CASCADE,
    id_textura INT REFERENCES texturas(id_textura) ON DELETE CASCADE
);
TABLA INTERMEDIA