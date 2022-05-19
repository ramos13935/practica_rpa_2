import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

"""
Antes de empezar debes abrir la powershell e ir a la carpeta dónde esté instalado chrome
 cd C:\"Program Files"\Google\Chrome\Application
Después hay que ejecutar chrome con este comando
 .\chrome.exe --remote-debugging-port=9999 --user-data-dir="C:\test"

"""


def start(lista_movimientos):
    driver = abrir_navegador()
    abrir_chat(driver, "FCT Practica 2")
    salir = False
    saludar(driver)
    correo = esperar_correo(driver)
    while not salir:
        menu(driver)
        opcion = recoger_opcion(driver)
        print("Opción start:", opcion)
        match opcion:
            case "1":
                print("entro a opción 1")
                mostrar_movimientos(driver, correo, lista_movimientos)
            case "2":
                pass
            case "3":
                pass
            case "0":
                salir = True
    mensaje_despedida = "¡Nos vemos pronto!"
    enviar_mensaje(driver, mensaje_despedida)


def enviar_mensaje(driver: webdriver, mensaje: str):
    barra_escribir_mensaje = driver.find_element(by=By.XPATH,
                                                 value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]")
    barra_escribir_mensaje.send_keys(mensaje, Keys.ENTER)
    print(mensaje)


def abrir_navegador():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.maximize_window()
    driver.get("https://web.whatsapp.com/")
    time.sleep(6)
    return driver


def abrir_chat(driver: webdriver, nombre_chat: str):
    chats = driver.find_elements_by_tag_name("span")
    for chat in chats:
        if chat.text == nombre_chat:
            chat.click()
            break


def esperar_correo(driver: webdriver):
    check = False
    correo = ""
    time.sleep(2)
    while not check:
        mensajes_usu = driver.find_elements(by=By.XPATH,
                                            value='//*[@id="main"]/div[3]/div/div[2]/div/div/div/div/div/div/div/span[@class="i0jNr selectable-text copyable-text"]/span')
        if "@" in mensajes_usu[-1].text:
            correo = mensajes_usu[-1].text
            check = True

    return correo


def saludar(driver: webdriver):
    mensaje_saludo = "Hola soy Jarvis, tu asistente.\nPara que podamos empezar, ¿podría indicarme su *correo electrónico*?"
    enviar_mensaje(driver, mensaje_saludo)


def menu(driver: webdriver):
    opciones_menu = "*1.* Consultar Movimientos\n*2.* ...\n*3.* Hablar con un agente\n*0.* Finalizar"
    enviar_mensaje(driver, opciones_menu)


def recoger_opcion(driver: webdriver):
    check = False
    opcion = ""
    while not check:
        mensajes_usu = driver.find_elements(by=By.XPATH,
                                            value='//*[@id="main"]/div[3]/div/div[2]/div/div/div/div/div/div/div/span[@class="i0jNr selectable-text copyable-text"]/span')

        if "0. Finalizar" not in mensajes_usu[-1].text:
            opcion = mensajes_usu[-1].text
            check = True

    return opcion


def mostrar_movimientos(driver: webdriver, correo: str, lista_movimientos):
    mensaje = ""
    print("Mostrar movimientos: ", correo)
    for movimiento in lista_movimientos:
        if movimiento.email == correo:
            mensaje += movimiento.__str__()+"\n"

    print("Movimientos totales:", mensaje)

    enviar_mensaje(driver, mensaje)

