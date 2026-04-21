import os
import time
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def login_and_save_cookies(driver, username, password, filepath):
    print("Iniciando sesión automáticamente...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)  # Esperar a que cargue la página de login

    try:
        # Localizar los campos de usuario y contraseña soportando variaciones del form
        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username'], input[name='email']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password'], input[name='pass']")

        # Escribir el usuario carácter por caracter
        for char in username:
            username_field.send_keys(char)
            time.sleep(0.1)  # Pequeño retraso entre teclas
        
        time.sleep(1)

        # Escribir la contraseña carácter por caracter
        for char in password:
            password_field.send_keys(char)
            time.sleep(0.1)

        time.sleep(1)

        # Enviar el formulario usando Enter sobre el campo de contraseña
        password_field.send_keys(Keys.RETURN)
        
        print("⏳ Esperando a que se complete el login...")
        time.sleep(10)  # Esperar a que redirija tras el login

        # Guardar las cookies
        cookies = driver.get_cookies()
        with open(filepath, "wb") as f:
            pickle.dump(cookies, f)
        print("✅ Inicio de sesión exitoso y cookies guardadas.")
        return True

    except Exception as e:
        print(f"❌ Error al intentar iniciar sesión: {e}")
        return False

def load_cookies(driver, filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("✅ Cookies cargadas exitosamente.")
        return True
    else:
        print("ℹNo se encontró el archivo de cookies. Se intentará iniciar sesión y generarlas.")
        return False

def download_image(url, folder_path, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(folder_path, filename), 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except Exception as e:
        print(f"Error descargando {url}: {e}")
    return False

def main():
    # Pedir datos al usuario
    tag = input("Ingresa el tag/hashtag a buscar: ")
    try:
        max_images = int(input("Ingresa la cantidad de imágenes a descargar: "))
    except ValueError:
        print("La cantidad debe ser un número entero.")
        return
    
    dir_name = input(f"Ingresa el nombre del directorio (opcional, por defecto será '{tag}'): ")
    if not dir_name.strip():
        dir_name = tag

    # Crear la ruta completa descargas/dir_name
    folder_path = os.path.join("descargas", dir_name)

    # Crear directorio si no existe
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Directorio '{folder_path}' creado.")
    else:
        print(f"📁 Las imágenes se guardarán en el directorio existente '{folder_path}'.")

    # Configurar Selenium
    options = Options()
    # options.add_argument('--headless') # Opcional: Ejecutar en segundo plano sin UI
    options.add_argument('--disable-notifications')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Intentar cargar cookies si existen
        driver.get("https://www.instagram.com/robots.txt")
        time.sleep(2)
        if not load_cookies(driver, "cookies"):
            # Si no hay cookies, obtener variables e iniciar sesión
            ig_user = os.getenv("IG_USERNAME")
            ig_pass = os.getenv("IG_PASSWORD")
            
            if not ig_user or not ig_pass:
                print("❌ Faltan credenciales IG_USERNAME e IG_PASSWORD en el archivo .env")
                return
            
            login_and_save_cookies(driver, ig_user, ig_pass, "cookies")

        # Ir a la página de búsqueda
        search_url = f"https://www.instagram.com/explore/search/keyword/?q={tag}"
        print(f"🔍 Navegando a: {search_url}")
        driver.get(search_url)
        time.sleep(5)  # Esperar a que cargue la página inicialmente

        image_urls = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        print("🌐 Extrayendo imágenes...")
        while len(image_urls) < max_images:
            # Parsear el HTML actual con BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            images = soup.find_all('img')

            for img in images:
                src = img.get('src')
                # Filtrar imágenes para evitar iconos pequeños o no válidos
                if src and src.startswith('https') and len(image_urls) < max_images:
                    # Las imagenes del grid de Instagram suelen estar bajo dominios como scontent o similares,
                    # se agregan al set para evitar duplicados.
                    if 'scontent' in src or 'instagram' in src:
                        image_urls.add(src)

            if len(image_urls) >= max_images:
                break

            # Hacer scroll hacia abajo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Esperar a que carguen nuevas imágenes
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Llegamos al final de la página o no cargan más imágenes. Se descargará lo encontrado.")
                break
            last_height = new_height

        print(f"✅ Se encontraron {len(image_urls)} imágenes. Iniciando descarga...")

        # Descargar imágenes
        for i, url in enumerate(image_urls, start=1):
            filename = f"{tag}_{i}.jpg"
            success = download_image(url, folder_path, filename)
            if success:
                print(f"⬇️ {i}/{len(image_urls)} descargada: {filename}")
            else:
                print(f"❌ Fallo al descargar: {url}")
                
    finally:
        print("Cerrando el navegador...")
        driver.quit()
        print("Proceso finalizado.")

if __name__ == "__main__":
    main()
