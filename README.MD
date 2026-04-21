# Descargar multiples imagenes de Instagram

Script para descargar multiples imagenes de un **tag/hashtag** de instagram usando webscraping

# Requisitos
- Tener un archivo `.env` con las credenciales de acceso a instagram

# Utilidades
- Url base: `https://www.instagram.com/explore/search/keyword/?q={tag}`

## Funcionamiento
- Se ejecuta el script
- Pregunta en la consola el tag
- pregunta la cantidad de imagenes de descagar
- pregunta el nombre del directorio donde se guardaran las imagenes (si existe los aguarda ahí, caso contrario crea el directorio)
- Descarga las imagenes