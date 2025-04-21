# codigo completo de insercion y actualizacion de datos tras los scrapeos

import pandas as pd
import psycopg2
import numpy as np

# Conexión
conn = psycopg2.connect(
    dbname="prueba_sephora",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Leer CSV
df = pd.read_csv("productos_maquillaje.csv")
pd.set_option('display.max_columns', None)

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
    
    efecto_sombra = row.get('efecto_sombra')
    textura = row.get('textura')

    # 1. ¿Existe el producto?
    cur.execute("SELECT id_producto FROM productos WHERE nombre = %s", (nombre,))
    producto_result = cur.fetchone()

    if producto_result:
        id_producto = producto_result[0]
        # Solo insertar histórico
        cur.execute("""
            INSERT INTO historico (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, numero_variaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones))
        print(f"Histórico actualizado para producto existente: {nombre}")
    else:
        # 2. Insertar Marca si no existe
        cur.execute("SELECT id_marca FROM marcas WHERE nombre_marca = %s", (marca,))
        marca_result = cur.fetchone()
        if marca_result:
            id_marca = marca_result[0]
        else:
            cur.execute("INSERT INTO marcas (nombre_marca) VALUES (%s) RETURNING id_marca", (marca,))
            id_marca = cur.fetchone()[0]

        # 3. Insertar Categoría si no existe
        cur.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = %s", (categoria,))
        categoria_result = cur.fetchone()
        if categoria_result:
            id_categoria = categoria_result[0]
        else:
            cur.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s) RETURNING id_categoria", (categoria,))
            id_categoria = cur.fetchone()[0]

        # 4. Insertar Subcategoría si no existe
        cur.execute("SELECT id_subcategoria FROM subcategorias WHERE nombre_subcategoria = %s", (subcategoria,))
        subcategoria_result = cur.fetchone()
        if subcategoria_result:
            id_subcategoria = subcategoria_result[0]
        else:
            cur.execute("INSERT INTO subcategorias (nombre_subcategoria) VALUES (%s) RETURNING id_subcategoria", (subcategoria,))
            id_subcategoria = cur.fetchone()[0]

        # 5. Insertar Producto
        cur.execute("""
            INSERT INTO productos (nombre, descripcion, id_marca, id_categoria, id_subcategoria)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_producto
        """, (nombre, descripcion, id_marca, id_categoria, id_subcategoria))
        id_producto = cur.fetchone()[0]

        # 6. Insertar Histórico
        cur.execute("""
            INSERT INTO historico (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, numero_variaciones)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_producto, fecha_extraccion, precio, numero_valoraciones, valoracion, num_variaciones))
        
        # 7. Insertar Filtros si existen
        # Efecto sombra
        if pd.notna(efecto_sombra):
            efectos = [e.strip() for e in efecto_sombra.split(",")]
            for efecto in efectos:
                cur.execute("SELECT id_efecto_sombra FROM efectos_sombra WHERE nombre_efecto = %s", (efecto,))
                efecto_result = cur.fetchone()
                if not efecto_result:
                    cur.execute("INSERT INTO efectos_sombra (nombre_efecto) VALUES (%s) RETURNING id_efecto_sombra", (efecto,))
                    id_efecto = cur.fetchone()[0]
                else:
                    id_efecto = efecto_result[0]
                cur.execute("INSERT INTO producto_efecto_sombra (id_producto, id_efecto_sombra) VALUES (%s, %s)", (id_producto, id_efecto))

        # Textura
        if pd.notna(textura):
            cur.execute("SELECT id_textura FROM texturas WHERE nombre_textura = %s", (textura,))
            textura_result = cur.fetchone()
            if not textura_result:
                cur.execute("INSERT INTO texturas (nombre_textura) VALUES (%s) RETURNING id_textura", (textura,))
                id_textura = cur.fetchone()[0]
            else:
                id_textura = textura_result[0]
            cur.execute("INSERT INTO producto_textura (id_producto, id_textura) VALUES (%s, %s)", (id_producto, id_textura))

        print(f"Producto nuevo insertado: {nombre}")

    conn.commit()

# Cerrar conexión
cur.close()
conn.close()
print("Proceso finalizado ✅")