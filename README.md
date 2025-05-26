# 💄 Análisis del Catálogo de Sephora y Propuesta de Nuevos Lanzamientos para Sephora Collection
Este proyecto tiene como objetivo analizar el catálogo de productos de maquillaje de la tienda online de Sephora, con foco específico en su línea propia Sephora Collection, para extraer información clave que permita tomar decisiones estratégicas sobre el portafolio actual y plantear posibles propuestas de nuevos productos. A través de un pipeline ETL completo, análisis exploratorio y visualizaciones interactivas, se construye una herramienta de apoyo a decisiones basada en datos reales del sitio web.

El punto de partida fue un proceso de web scraping automatizado para extraer los datos de productos de maquillaje desde la web oficial de Sephora España. Estos datos fueron posteriormente limpiados, transformados y almacenados de forma estructurada para facilitar su análisis. Para un mayor detalle sobre el proceso ETL y su desarrollo, se recomienda consultar el informe final, donde se describe el procedimiento. Con esta base sólida, se desarrolló un análisis exploratorio de datos (EDA) que permitió detectar patrones, correlaciones y oportunidades relevantes en el catálogo, centrando el foco en los factores asociados al éxito comercial de los productos.

Finalmente, toda esta información se tradujo en un dashboard interactivo desarrollado en Power BI, el cual permite explorar los hallazgos del análisis y visualizar tres propuestas de lanzamiento con tres enfoques diferentes: lanzamiento seguro, arriesgado y de mejora. El informe final recoge todos los aprendizajes, decisiones técnicas y posibles caminos futuros para escalar o refinar el proyecto.

## 📂 Estructura del Proyecto

├── data/                          
│   ├── productos_maquillaje.csv       # Dataset final extraído del sitio web de Sephora
│  
├── documentacion/                 # Documentos PDF entregables del proyecto 
│   ├── Definicion_Proyecto.pdf         
│   ├── EDA_Proyecto.pdf    
│   ├── ETL_Proyecto.pdf         
│   ├── Dashboard_Proyecto.pdf             
│   ├── Informe_Final.pdf      
│  
├── src/etl/                       # Funciones de soporte para la ETL  
│   ├── extract_transf.py          # Funciones para la extracción y transformación
│   ├── load.py                    # Funciones para la carga en la base de datos
│   ├── init.py 
│   ├── main.py                    # Script central que orquesta todo el proceso ETL
│ 
├── eda.ipynb                      # Análisis exploratorio de los datos 
├── Dashboard_Sephora.pbix         # Archivo Power BI con el dashboard final
├── esquema_bd.md                  # Estructura de la base de datos utilizada
├── requirements.txt               # Dependencias del entorno Python 
├── .gitignore                     # Archivo para ignorar archivos innecesarios en el repositorio  
├── README.md                      # Descripción del proyecto  

## 💻 Instalación y Requisitos

Este proyecto fue desarrollado en Python 3.13.0 y utiliza diversas herramientas para llevar a cabo el scraping, procesamiento, análisis y visualización de datos. A continuación se detallan los componentes clave:

🔧 Tecnologías y Herramientas
- Python: Lenguaje principal para la extracción, transformación, análisis y conexión a la base de datos.
- PostgreSQL: Base de datos relacional utilizada para almacenar los datos estructurados.
- DBeaver: Cliente visual para la administración de la base de datos.
- Power BI: Herramienta de visualización utilizada para crear el dashboard final.

📦 Librerías Principales
- Web Scraping: selenium, webdriver-manager
- Procesamiento de Datos: pandas, numpy
- Análisis y Visualización: plotly
- Base de Datos: psycopg2, python-dotenv
- Otras utilidades: datetime, os, time, re, json

## 📊 Principales Resultados y Conclusiones del Análisis

- Posicionamiento general de Sephora Collection

Sephora Collection es la marca con mayor presencia dentro del catálogo de Sephora, con 198 productos que representan el 10,87% del total (1.822 productos). Se posiciona como una opción asequible, con un precio mediano de 13,99 €, muy por debajo del precio mediano general (34,99 €). A pesar de su enfoque económico, la marca mantiene una valoración mediana elevada de 4,4 sobre 5, equivalente a la media de toda la tienda, lo que evidencia su buena percepción por parte de los usuarios. Su índice de éxito interno es del 16,16%, y aporta un 8,14% del total de productos exitosos, siendo la segunda marca con mayor contribución, solo por detrás de Benefit. La correlación entre precio y éxito en Sephora Collection es moderada (0,31), indicando que, aunque un precio competitivo puede ayudar, no es el único factor que determina el rendimiento de un producto. En términos de cobertura, está presente en 40 de las 48 subcategorías, con especial dominio en brochas de rostro, sombras de ojos y máscaras de pestañas, mientras que no tiene presencia en otras como paletas de contouring/multiusos, cremas BB & CC, estuches de rostro/ceja/ojos o geles de uñas, lo que señala oportunidades claras de expansión.

- Propuestas de lanzamiento para Sephora Collection 
    - Lanzamiento seguro: Brocha de rostro 
    Sephora Collection lidera con solidez la subcategoría de brochas de rostro, con una alta tasa de éxito interna donde cerca del 48% de sus productos son exitosos. Estos productos destacan por ser simples y rentables, con poca variabilidad en diseño. Aunque la saturación de la subcategoría es considerable, esta situación puede mitigarse mediante una diferenciación clara, ya sea a través de funcionalidades innovadoras, colaboraciones especiales o packaging sostenible. Se recomienda posicionar el precio en un rango medio-alto para aumentar el valor percibido sin perder su identidad económica.
    - Lanzamiento arriesgado: Crema BB & CC 
    Esta subcategoría representa una oportunidad de lanzamiento para Sephora Collection, ya que actualmente no tiene presencia en ella. Se trata de un segmento con una tasa de éxito alta dentro de Sephora, dominado por marcas como Erborian, que se posicionan con precios más elevados. Se sugiere introducir un producto básico, sin variaciones, que ofrezca una fórmula sencilla y universal a un precio competitivo inferior al de los líderes, para captar consumidores que buscan calidad a buen precio. La estrategia debe incluir una comunicación clara y educativa para compensar la falta de reconocimiento en esta categoría.
    - Lanzamiento de mejora: Sombra de ojos 
    Aunque Sephora Collection cuenta con la mayor cantidad de sombras dentro de Sephora, su tasa de éxito es relativamente baja y presenta valoraciones inferiores en comparación con la competencia. Se observa que ofrecer muchas variaciones no mejora el rendimiento; por el contrario, los productos exitosos tienen menos variaciones y un precio ligeramente superior. Esto indica que el precio bajo no basta para asegurar el éxito. Por ello, se recomienda enfocar los futuros lanzamientos en mejorar la calidad de la fórmula, el packaging y la experiencia del usuario, apostando por paletas compactas y versátiles que incrementen la percepción de valor.

Para un análisis más detallado de los resultados y una visión completa de todas las métricas y hallazgos, se recomienda consultar el informe final, donde se presentan en profundidad todos los datos y análisis realizados. Además, para facilitar la exploración y permitir la interacción dinámica con los resultados, está disponible un dashboard interactivo que ofrece visualizaciones intuitivas y actualizadas del catálogo y desempeño de Sephora Collection y otras marcas dentro de Sephora.

## 💡Próximos Pasos

- Precio por unidad: Incluir el precio por mililitro o gramo (€/ml o €/g) permitiría comparaciones más precisas y un análisis más justo del posicionamiento de precio entre productos.
- Calidad de atributos: Mejorar la limpieza de campos como formato, acabado o textura, cuya fiabilidad fue limitada por la estructura de la web. También se podría reintentar la extracción de ingredientes aplicando técnicas de NLP.
- Carga de datos: Revisar el proceso de inserción en la base de datos, ya que se detectaron duplicados inesperados en la primera carga. La base está preparada para almacenar nuevos datos y facilitar análisis temporales futuros.
- Dashboard: Ampliar el dashboard con una sección dedicada al análisis de outliers y, si se dispone de más histórico, visualizar la evolución temporal de productos.
- Código y documentación: Modularizar funciones del EDA, automatizar generación de resultados clave y mejorar la documentación (docstrings y estructura) en scripts ETL y notebooks.

## 🤝 Contribuciones
Agradezco cualquier contribución que pueda mejorar el proyecto. Si tienes alguna idea que aportar no dudes en contactar conmigo!
- LinkedIn: www.linkedin.com/in/raquelsanchezcv 
- Correo electrónico: raquelscv@gmail.com

## 👤 Autor 
**Raquel Sánchez** - https://github.com/raquelscv 