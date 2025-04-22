import pandas as pd
import psycopg2

def conectar_bd(nombre_db, usuario, contraseña, servidor, puerto):
    conn = psycopg2.connect(
        dbname=nombre_db,
        user=usuario,
        password=contraseña,
        host=servidor,
        port=puerto
    )
    return conn, conn.cursor()

def insertar_historico(cur, id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones):
    cur.execute("""
        INSERT INTO historico (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, numero_variaciones)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones))

def obtener_id(cur, tabla, columna, valor):
    columnas_id = {
        'marcas': 'id_marca',
        'categorias': 'id_categoria',
        'subcategorias': 'id_subcategoria',
        'efectos_sombra': 'id_efecto_sombra',
        'texturas': 'id_textura',
        'formatos': 'id_formato',
        'responsabilidades': 'id_responsabilidad',
        'efectos_labios': 'id_efecto_labios',
        'efectos_mascara': 'id_efecto_mascara',
        'formulaciones': 'id_formulacion',
        'tipos_piel': 'id_tipo_piel',
        'coberturas': 'id_cobertura',
        'acabados': 'id_acabado'
    }
    
    columna_id = columnas_id.get(tabla)
    
    if not columna_id:
        raise ValueError(f"No se ha definido columna 'id' para la tabla {tabla}")

    print(f"Ejecutando consulta: SELECT {columna_id} FROM {tabla} WHERE {columna} = {valor}")
    cur.execute(f"SELECT {columna_id} FROM {tabla} WHERE {columna} = %s", (valor,))
    return cur.fetchone()

def insertar_categoria_subcategoria_marca(cur, marca, categoria, subcategoria):
    id_marca = obtener_id(cur, "marcas", "nombre_marca", marca)
    if not id_marca:
        cur.execute("INSERT INTO marcas (nombre_marca) VALUES (%s) RETURNING id_marca", (marca,))
        id_marca = cur.fetchone()[0]

    id_categoria = obtener_id(cur, "categorias", "nombre_categoria", categoria)
    if not id_categoria:
        cur.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s) RETURNING id_categoria", (categoria,))
        id_categoria = cur.fetchone()[0]

    id_subcategoria = obtener_id(cur, "subcategorias", "nombre_subcategoria", subcategoria)
    if not id_subcategoria:
        cur.execute("INSERT INTO subcategorias (nombre_subcategoria) VALUES (%s) RETURNING id_subcategoria", (subcategoria,))
        id_subcategoria = cur.fetchone()[0]

    return id_marca, id_categoria, id_subcategoria

def insertar_producto(cur, nombre, descripcion, id_marca, id_categoria, id_subcategoria):
    cur.execute("""
        INSERT INTO productos (nombre, descripcion, id_marca, id_categoria, id_subcategoria)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_producto
    """, (nombre, descripcion, id_marca, id_categoria, id_subcategoria))
    return cur.fetchone()[0]

def insertar_filtro(cur, filtro, tabla, producto_id, relacion_tabla):
    if pd.notna(filtro):
        filtros = [f.strip() for f in filtro.split(",")]
        for f in filtros:
            try:
                id_filtro = obtener_id(cur, tabla, f"nombre_{tabla}", f)
                if not id_filtro:  # Si no existe, insertamos
                    cur.execute(f"INSERT INTO {tabla} (nombre_{tabla}) VALUES (%s) RETURNING id_{tabla}", (f,))
                    id_filtro = cur.fetchone()[0]
                if id_filtro:  # Asegurarse de que id_filtro no sea None
                    cur.execute(f"INSERT INTO producto_{relacion_tabla} (id_producto, id_{tabla}) VALUES (%s, %s)", (producto_id, id_filtro))
            except Exception as e:
                print(f"Error al insertar filtro {f} para producto {producto_id}: {e}")
                continue

def procesar_productos(df, cur):
    filtros = [
        ('efecto_sombra', 'efecto_sombra'),
        ('textura', 'textura'),
        ('formato', 'formato'),
        ('responsabilidad', 'responsabilidad'),
        ('efecto_labios', 'efecto_labios'),
        ('efecto_mascara', 'efecto_mascara'),
        ('formulacion', 'formulacion'),
        ('tipo_piel', 'tipo_piel'),
        ('cobertura', 'cobertura'),
        ('acabado', 'acabado')
    ]

    for _, row in df.iterrows():
        nombre = row['nombre']
        descripcion = row['descripcion']
        marca = row['marca']
        categoria = row['categoria']
        subcategoria = row['subcategoria']
        precio = row['precio']
        numero_valoraciones = row['numero_valoraciones']
        num_variaciones = row['num_variaciones']
        valoracion = row['valoracion']
        fecha_extraccion = row['fecha_extraccion']

        cur.execute("SELECT id_producto FROM productos WHERE nombre = %s", (nombre,))
        producto_result = cur.fetchone()

        if producto_result:
            id_producto = producto_result[0]
            insertar_historico(cur, id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones)
            print(f"Histórico actualizado para producto existente: {nombre}")
        else:
            id_marca, id_categoria, id_subcategoria = insertar_categoria_subcategoria_marca(cur, marca, categoria, subcategoria)
            id_producto = insertar_producto(cur, nombre, descripcion, id_marca, id_categoria, id_subcategoria)
            insertar_historico(cur, id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones)

            for filtro, tabla in filtros:
                insertar_filtro(cur, row.get(filtro), tabla, id_producto, filtro)

            print(f"Producto nuevo insertado: {nombre}")

def cargar_datos_sephora(df, nombre_db, usuario, contraseña, servidor, puerto):
    conn, cur = conectar_bd(nombre_db, usuario, contraseña, servidor, puerto)

    procesar_productos(df, cur)  
    conn.commit()  

    cur.close()
    conn.close()
    print("Proceso finalizado ✅")