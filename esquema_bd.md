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
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    url_producto TEXT,
    nombre TEXT,
    descripcion TEXT,
    id_marca INT REFERENCES marcas(id_marca) ON DELETE CASCADE,
    id_categoria INT REFERENCES categorias(id_categoria) ON DELETE CASCADE,
    id_subcategoria INT REFERENCES subcategorias(id_subcategoria) ON DELETE CASCADE
);
CREATE TABLE historico (
    id_extraccion SERIAL PRIMARY KEY,
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    fecha_extraccion DATE,
    precio FLOAT CHECK (precio >= 0),
    numero_valoraciones INT,
    valoracion FLOAT CHECK (valoracion BETWEEN 0 AND 5),
    numero_variaciones INT
);
CREATE TABLE formatos (
    id_formato SERIAL PRIMARY KEY,
    nombre_formato TEXT
);
CREATE TABLE producto_formato (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_formato INT REFERENCES formatos(id_formato) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_formato)
);
CREATE TABLE responsabilidades (
    id_responsabilidad SERIAL PRIMARY KEY,
    nombre_responsabilidad TEXT
);
CREATE TABLE producto_responsabilidad (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_responsabilidad INT REFERENCES responsabilidades(id_responsabilidad) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_responsabilidad)
);
CREATE TABLE efectos_sombra (
    id_efecto_sombra SERIAL PRIMARY KEY,
    nombre_efecto TEXT
);
CREATE TABLE producto_efecto_sombra (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_efecto_sombra INT REFERENCES efectos_sombra(id_efecto_sombra) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_efecto_sombra)
);
CREATE TABLE efectos_labios (
    id_efecto_labios SERIAL PRIMARY KEY,
    nombre_efecto TEXT
);
CREATE TABLE producto_efecto_labios (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_efecto_labios INT REFERENCES efectos_labios(id_efecto_labios) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_efecto_labios)
);
CREATE TABLE efectos_mascara (
    id_efecto_mascara SERIAL PRIMARY KEY,
    nombre_efecto TEXT 
);
CREATE TABLE producto_efecto_mascara (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_efecto_mascara INT REFERENCES efectos_mascara(id_efecto_mascara) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_efecto_mascara)
);
CREATE TABLE formulaciones (
    id_formulacion SERIAL PRIMARY KEY,
    nombre_formulacion TEXT
);
CREATE TABLE producto_formulacion (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_formulacion INT REFERENCES formulaciones(id_formulacion) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_formulacion)
);
CREATE TABLE tipos_piel (
    id_tipo_piel SERIAL PRIMARY KEY,
    nombre_tipo_piel TEXT
);
CREATE TABLE producto_tipo_piel (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_tipo_piel INT REFERENCES tipos_piel(id_tipo_piel) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_tipo_piel)
);
CREATE TABLE coberturas (
    id_cobertura SERIAL PRIMARY KEY,
    nombre_cobertura TEXT
);
CREATE TABLE producto_cobertura (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_cobertura INT REFERENCES coberturas(id_cobertura) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_cobertura)
);
CREATE TABLE acabados (
    id_acabado SERIAL PRIMARY KEY,
    nombre_acabado TEXT
);
CREATE TABLE producto_acabado (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_acabado INT REFERENCES acabados(id_acabado) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_acabado)
);
CREATE TABLE texturas (
    id_textura SERIAL PRIMARY KEY,
    nombre_textura TEXT
);
CREATE TABLE producto_textura (
    id_producto INT REFERENCES productos(id_producto) ON DELETE CASCADE,
    id_textura INT REFERENCES texturas(id_textura) ON DELETE CASCADE,
    PRIMARY KEY (id_producto, id_textura)
);