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

def obtener_o_insertar_id(cur, id_col, tabla, columna, valor):
    cur.execute(f"SELECT {id_col} FROM {tabla} WHERE {columna} = %s", (valor,))
    resultado = cur.fetchone()
    
    if resultado:
        return resultado[0]
    else:
        cur.execute(
            f"INSERT INTO {tabla} ({columna}) VALUES (%s) RETURNING {id_col}",
            (valor,)
        )
        return cur.fetchone()[0]

def insertar_producto(cur, nombre, descripcion, id_marca, id_categoria, id_subcategoria):
    cur.execute("""
        INSERT INTO productos (nombre, descripcion, id_marca, id_categoria, id_subcategoria)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_producto
    """, (nombre, descripcion, id_marca, id_categoria, id_subcategoria))
    return cur.fetchone()[0]

def insertar_filtro(cur, columna, id_col, tabla, nombre_col, id_producto, tabla_intermedia):
    if pd.notna(columna):
        filtros = [v.strip() for v in columna.split(",")]
        for v in filtros:
            cur.execute(f"SELECT {id_col} FROM {tabla} WHERE {nombre_col} = %s", (v,))
            resultado = cur.fetchone()

            if resultado:
                id_filtro = resultado[0]
            else:
                cur.execute(f"INSERT INTO {tabla} ({nombre_col}) VALUES (%s) RETURNING {id_col}", (v,))
                id_filtro = cur.fetchone()[0]

            cur.execute(f"INSERT INTO {tabla_intermedia} (id_producto, {id_col}) VALUES (%s, %s)", (id_producto, id_filtro))

def procesar_productos(df, cur):
    for _, row in df.iterrows():
        nombre = row['nombre'] if pd.notna(row['nombre']) else None
        descripcion = row['descripcion'] if pd.notna(row['descripcion']) else None
        marca = row['marca']
        categoria = row['categoria']
        subcategoria = row['subcategoria']
        precio = row['precio'] if pd.notna(row['precio']) else None
        numero_valoraciones = row['numero_valoraciones']
        num_variaciones = row['num_variaciones']
        valoracion = row['valoracion']
        fecha_extraccion = row['fecha_extraccion']
        efecto_sombra = row.get('efecto_sombra')
        textura = row.get('textura')
        formato = row.get('formato')
        responsabilidad = row.get('responsabilidad')
        efecto_labios = row.get('efecto_labios')
        efecto_mascara = row.get('efecto_mascara')
        formulacion = row.get('formulacion')
        tipo_piel = row.get('tipo_piel')
        cobertura = row.get('cobertura')
        acabado = row.get('acabado')

        cur.execute("SELECT id_producto FROM productos WHERE nombre = %s", (nombre,))
        producto_result = cur.fetchone()

        if producto_result:
            id_producto = producto_result[0]
            insertar_historico(cur, id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones)
            print(f"Histórico actualizado para producto existente: {nombre}")
        else:
            id_marca = obtener_o_insertar_id(cur, "id_marca", "marcas", "nombre_marca", marca) if pd.notna(marca) else None
            id_categoria = obtener_o_insertar_id(cur, "id_categoria", "categorias", "nombre_categoria", categoria) if pd.notna(categoria) else None
            id_subcategoria = obtener_o_insertar_id(cur, "id_subcategoria", "subcategorias", "nombre_subcategoria", subcategoria) if pd.notna(subcategoria) else None
            id_producto = insertar_producto(cur, nombre, descripcion, id_marca, id_categoria, id_subcategoria)
            insertar_historico(cur, id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones)
            insertar_filtro(cur, efecto_labios, "id_efecto_labios", "efectos_labios", "nombre_efecto", id_producto, "producto_efecto_labios")
            insertar_filtro(cur, efecto_sombra, "id_efecto_sombra", "efectos_sombra", "nombre_efecto", id_producto, "producto_efecto_sombra")
            insertar_filtro(cur, textura, "id_textura", "texturas", "nombre_textura", id_producto, "producto_textura")
            insertar_filtro(cur, formato, "id_formato", "formatos", "nombre_formato", id_producto, "producto_formato")  
            insertar_filtro(cur, responsabilidad, "id_responsabilidad", "responsabilidades", "nombre_responsabilidad", id_producto, "producto_responsabilidad")
            insertar_filtro(cur, efecto_mascara, "id_efecto_mascara", "efectos_mascara", "nombre_efecto", id_producto, "producto_efecto_mascara")
            insertar_filtro(cur, formulacion, "id_formulacion", "formulaciones", "nombre_formulacion", id_producto, "producto_formulacion")
            insertar_filtro(cur, tipo_piel, "id_tipo_piel", "tipos_piel", "nombre_tipo_piel", id_producto, "producto_tipo_piel")
            insertar_filtro(cur, cobertura, "id_cobertura", "coberturas", "nombre_cobertura", id_producto, "producto_cobertura")    
            insertar_filtro(cur, acabado, "id_acabado", "acabados", "nombre_acabado", id_producto, "producto_acabado")

def cargar_datos_sephora(df, nombre_db, usuario, contraseña, servidor, puerto):
    conn, cur = conectar_bd(nombre_db, usuario, contraseña, servidor, puerto)

    procesar_productos(df, cur)  
    conn.commit()  

    cur.close()
    conn.close()
    print("Proceso finalizado ✅")