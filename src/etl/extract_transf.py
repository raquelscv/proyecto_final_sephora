from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time, json, re
import numpy as np
import pandas as pd
from datetime import date

def iniciar_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_script_timeout(100)
    return driver

def cargar_todos_los_productos(driver, mostrar_productos=True, mostrar_scroll=True):
    try:
        ver_mas_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'see-more-button') and contains(@class, 'secondary-button-revamp')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ver_mas_btn)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", ver_mas_btn)
        if mostrar_productos:
            print("🔘 Botón 'Ver más' clicado.")
    except:
        if mostrar_productos:
            print("ℹ️ No se encontró botón 'Ver más'.")

    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(200):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if mostrar_scroll:
            productos = len(driver.find_elements(By.CLASS_NAME, 'product-brand'))
            print(f"[Scroll {i}] Scroll height: {new_height} - Productos: {productos}")
        if new_height == last_height and i > 5:
            break
        last_height = new_height

def obtener_urls_productos(driver):
    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "product-tile.clickable.omnibus-tile"))
    )
    urls = []
    for producto in productos:
        data = producto.get_attribute('data-tcproduct')
        if data:
            prod_data = json.loads(data)
            url = prod_data.get('product_url_page')
            url = re.sub(r'-p(\d+)\.html$', r'-P\1.html', url)
            urls.append(url)
    return urls

def obtener_urls_filtros(driver, palabras_clave):
    filtros_urls = []
    filtros = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gtmrefinement.empty.refinement-item")))
    for f in filtros:
        href = f.get_attribute("href")
        if href and any(p in href for p in palabras_clave):
            filtros_urls.append(href)
    return filtros_urls

def scrapeo_filtros(driver, filtros_urls, mapa_filtros):
    productos_por_filtro = {col: [] for col in mapa_filtros.values()}
    for filtro_url in filtros_urls:
        driver.get(filtro_url)
        time.sleep(3)
        cargar_todos_los_productos(driver, mostrar_scroll=False)

        try:
            valor = driver.find_element(By.CLASS_NAME, "breadcrumb-refinement-value").text.strip()
        except:
            valor = "Valor desconocido"

        productos_en_filtro = []
        productos = driver.find_elements(By.CLASS_NAME, "product-tile.clickable.omnibus-tile")
        for p in productos:
            data = p.get_attribute('data-tcproduct')
            if data:
                prod_data = json.loads(data)
                url_producto = prod_data.get('product_url_page')
                if url_producto:
                    url_producto = re.sub(r'-p(\d+)\.html$', r'-P\1.html', url_producto)
                    productos_en_filtro.append(url_producto)

        for clave, columna in mapa_filtros.items():
            if clave in filtro_url:
                productos_por_filtro[columna].append({"valor": valor, "productos": productos_en_filtro})
                print(f"🔹 Filtro: {columna} | Valor: {valor} | Productos: {len(productos_en_filtro)}")
                break

    return productos_por_filtro

def scrapeo_producto(driver, product_url, productos_por_filtro):
    producto_info = {}
    driver.get(product_url)

    try:
        breadcrumb_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "breadcrumb-element"))
        )
        if len(breadcrumb_elements) < 2 or breadcrumb_elements[1].text.strip() != "Maquillaje":
            print(f"⛔ Producto fuera de 'Maquillaje'. Saltando: {product_url}")
            return None
    except:
        print(f"⚠️ No se pudo obtener breadcrumb del producto: {product_url}")
        return None
    
    try:
        producto_info["categoria"] = breadcrumb_elements[2].text.strip()
    except:
        producto_info["categoria"] = np.nan

    try:
        producto_info["subcategoria"] = breadcrumb_elements[3].text.strip()
    except:
        producto_info["subcategoria"] = np.nan

    try:
        producto_info["marca"] = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "brand-name"))).text
    except:
        producto_info["marca"] = np.nan

    try:
        titulo = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-name.product-name-bold"))
        )[0].text.strip().replace("\n", " ")

        if " - " in titulo:
            partes = titulo.split(" - ", 1)
            nombre = partes[0].strip()
            descripcion = partes[1].strip()
        else:
            nombre = titulo
            descripcion = np.nan

        producto_info["nombre"] = nombre
        producto_info["descripcion"] = descripcion

    except Exception as e:
        print(f"⚠️ Error extrayendo título del producto: {e}")
        return None

    try:
        precio = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "price-sales.price-sales-standard")))[0].text
        producto_info["precio"] = float(precio.replace(" €", "").replace(",", "."))
    except:
        producto_info["precio"] = np.nan

    try:
        n_val = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bv-number-review"))).get_attribute('innerHTML').strip().split(' ')[0]
        producto_info["numero_valoraciones"] = int(n_val)
    except:
        producto_info["numero_valoraciones"] = 0

    try:
        contenido = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bv-overall-score"))).get_attribute('innerHTML')
        valoracion = re.search(r"\d+\.\d+/5", contenido).group(0).split("/")[0]
        producto_info["valoracion"] = float(valoracion)
    except:
        producto_info["valoracion"] = 0

    variaciones = 0
    try:
        tonos = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "open-colorguide"))).text.split('(')[1].split(')')[0]
        variaciones = int(tonos)
    except:
        pass
    try:
        tamanos = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CLASS_NAME, "open-selector"))).text.split('(')[1].split(')')[0]
        variaciones = int(tamanos)
    except:
        pass
    producto_info["num_variaciones"] = variaciones

    producto_info["fecha_extraccion"] = pd.to_datetime(date.today())

    try: 
        for columna, filtros in productos_por_filtro.items():
            valores_detectados = []
            for filtro in filtros:
                if product_url in filtro["productos"]:
                    valores_detectados.append(filtro["valor"])
            producto_info[columna] = ", ".join(valores_detectados) if valores_detectados else None
    except Exception as e:
        print(f"⚠️ Error procesando filtros personalizados: {e}")

    return producto_info

def scrapeo_sephora(url, archivo_salida):
    palabras_clave = ["formats", "responsibleBeauty", "eyeshadowEffects", "lipEffects", "mascaraEffects", "formulations", "skinTypes", "covers", "finishes", "texture"]
    mapa_filtros = {
        "formats": "formato",
        "responsibleBeauty": "responsabilidad",
        "eyeshadowEffects": "efecto_sombra",
        "lipEffects": "efecto_labios",
        "mascaraEffects": "efecto_mascara",
        "formulations": "formulacion",
        "skinTypes": "tipo_piel",
        "covers": "cobertura",
        "finishes": "acabado",
        "texture": "textura"
    }

    driver = iniciar_driver()
    driver.get(url)
    cargar_todos_los_productos(driver)
    productos_urls = obtener_urls_productos(driver)
    print(f"\n🟢 Productos en página principal: {len(productos_urls)}")
    driver.quit()

    driver = iniciar_driver()
    driver.get(url)
    filtros_urls = obtener_urls_filtros(driver, palabras_clave)
    print(f"\n🔍 Filtros encontrados: {len(filtros_urls)}")
    driver.quit()

    driver = iniciar_driver()
    productos_por_filtro = scrapeo_filtros(driver, filtros_urls, mapa_filtros)
    driver.quit()

    list_scrap = []
    driver = iniciar_driver()
    for idx, product_url in enumerate(productos_urls):
        print(f"📦 Procesando producto {idx+1} de {len(productos_urls)}: {product_url}")
        info = scrapeo_producto(driver, product_url, productos_por_filtro)
        if info:
            list_scrap.append(info)
    driver.quit()

    df = pd.DataFrame(list_scrap)
    df.to_csv(archivo_salida)
    print(f"✅ CSV guardado como {archivo_salida}")

    return df 