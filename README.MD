# Descargar múltiples imágenes de Instagram

Script para descargar múltiples imágenes de un **tag/hashtag** de instagram usando web scraping con Selenium y BeautifulSoup.

> **⚠️ Advertencia Legal y de Uso:** Este proyecto tiene fines puramente educativos. El scraping de Instagram va en contra de sus Términos de Servicio. El uso excesivo o inadecuado de este script puede resultar en el bloqueo temporal o permanente de tu cuenta de Instagram o de tu dirección IP. Úsalo bajo tu propia responsabilidad.

## Requisitos Previos
- Python 3.8+ instalado en tu sistema.
- Google Chrome instalado.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con tus credenciales de acceso a Instagram:

```env
IG_USERNAME=tu_usuario
IG_PASSWORD=tu_contraseña
```

## Utilidades y Autenticación
- **Url base:** `https://www.instagram.com/explore/search/keyword/?q={tag}`
- **Login Automático:** El script utiliza la URL de `https://www.instagram.com/robots.txt` como terreno seguro para inyectar cookies. 
- Si no posees un archivo `cookies` generado previamente, el script automatizará el inicio de sesión utilizando tus credenciales de `.env` y generará el archivo binario de `cookies` localmente para agilizar futuros inicios de sesión y evitar bloqueos.

## Uso y Funcionamiento

Ejecuta el script principal:
```bash
python main.py
```

El script te solicitará la siguiente información de forma interactiva:
1. **Tag/Hashtag** a buscar.
2. **Cantidad** de imágenes a descargar.
3. **Nombre del directorio** donde se guardarán las imágenes. Si se deja en blanco, se creará uno con el nombre del tag. (Los archivos se depositarán dentro de una carpeta principal llamada `descargas/`).