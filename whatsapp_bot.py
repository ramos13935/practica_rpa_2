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
        menu(driver, correo, lista_movimientos)
        opcion = recoger_ultimo_mensaje(driver)
        if opcion == "1":
            submenu_movimientos(driver, correo, lista_movimientos)
        elif opcion == "2":
            pass
        elif opcion == "3":
            enviar_mensaje(driver, ["Puede llamar al 12345679 (L-V, 8:00-21:00) para obtener más información"])
            salir = True

        elif opcion == "0":
            salir = True
        else:
            enviar_mensaje(driver, ["Por favor escriba una de las opciones válidas"])

    mensaje_despedida = "¡Nos vemos pronto!"
    enviar_mensaje(driver, [mensaje_despedida])


def menu(driver: webdriver, correo, lista_movimientos):
    nombre = "Bienbenido/a " + get_nombre(correo, lista_movimientos) + " las opciones disponibles son:"
    op1 = "*1.* Movimientos"
    op2 = "*2.* ..."
    op3 = "*3.* Hablar con un agente"
    op0 = "*0.* Finalizar"
    enviar_mensaje(driver, [nombre, op1, op2, op3, op0])


def submenu_movimientos(driver, correo, lista_movimientos):
    tit = "*MOVIMIENTOS*"
    op1 = "*1.* Buscar movimiento"
    op2 = "*2.* Mostrar movimientos "
    op0 = "*0.* Volver al menú principal"
    flag = True
    while flag:
        enviar_mensaje(driver, [tit, op1, op2, op0])
        resp = recoger_ultimo_mensaje(driver)
        if resp == "1":
            mostrar_movimiento(driver, correo, lista_movimientos)
        elif resp == "2":
            mostrar_movimientos(driver, correo, lista_movimientos)
        elif resp == "0":
            flag = False
        else:
            enviar_mensaje(driver, ["No es una opción valida, escriba una de las opciones "])


def escribir_emoticono(driver: webdriver, emoticono: str):
    barra_escribir_mensaje = driver.find_element(by=By.XPATH,
                                                 value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]")
    barra_escribir_mensaje.send_keys(emoticono, Keys.ENTER)


def enviar_mensaje(driver: webdriver, mensajes: list):
    barra_escribir_mensaje = driver.find_element(by=By.XPATH,
                                                 value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]")
    for mensaje in mensajes:
        if mensaje[0] == ":":
            barra_escribir_mensaje.send_keys(mensaje, Keys.ENTER)
            barra_escribir_mensaje.send_keys("", Keys.SHIFT + Keys.ENTER)
        else:
            barra_escribir_mensaje.send_keys(mensaje, Keys.SHIFT + Keys.ENTER)

    btn_enviar = driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span[@data-testid="send"]')
    btn_enviar.click()
    time.sleep(1)


def abrir_navegador():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.maximize_window()
    driver.get("https://web.whatsapp.com/")
    time.sleep(5)
    return driver


def abrir_chat(driver: webdriver, nombre_chat: str):
    chats = driver.find_elements_by_tag_name("span")
    for chat in chats:
        if chat.text == nombre_chat:
            chat.click()
            break
    time.sleep(2)


def esperar_correo(driver: webdriver):
    flag = True
    correo = ""
    while flag:
        correo = recoger_ultimo_mensaje(driver)
        if "@" in correo:
            flag = False
        else:
            enviar_mensaje(driver, ["Escriba un *correo electrónico* válido por favor."])

    return correo


def saludar(driver: webdriver):
    l1 = "Hola, soy Jarvis, tu asistente."
    em = ":saludar"
    l2 = "Para que podamos empezar, ¿podría indicarme su *correo electrónico*?"
    enviar_mensaje(driver, [l1, em, l2])


def recoger_ultimo_mensaje(driver: webdriver):
    check = False
    ultimo_mensaje = ""
    value_mensajes = '//*[@id="main"]/div[3]/div/div[2]/div/div/div/div/div/div/div/span[@class="i0jNr selectable-text copyable-text"]/span'
    contador_mesajes = len(driver.find_elements(by=By.XPATH, value=value_mensajes))
    while not check:
        mensajes_usu = driver.find_elements(by=By.XPATH,
                                            value=value_mensajes)

        if len(mensajes_usu) > contador_mesajes:
            ultimo_mensaje = mensajes_usu[-1].text
            check = True

        # time.sleep(0.5)
    return ultimo_mensaje


def mostrar_movimiento(driver, correo, lista_movimientos):
    flag = True
    while flag:
        enviar_mensaje(driver, ["Escribe el código del movimiento que quiere revisar:"])
        cod_mov = recoger_ultimo_mensaje(driver)
        mensaje = ["*_Datos del movimiento:*_"]
        permiso = True
        for movimiento in lista_movimientos:
            if str(movimiento.codigo_operacion) == cod_mov and correo == movimiento.email:
                mensaje.append(movimiento.__str__())
                break
            elif str(movimiento.codigo_operacion) == cod_mov and correo != movimiento.email:
                enviar_mensaje(driver, ["No tienes permiso para ver ese movimiento"])
                permiso = False
                break

        if permiso and len(mensaje) > 1:
            enviar_mensaje(driver, mensaje)
        elif permiso:
            enviar_mensaje(driver, ["Código de operación no encontrado"])

        enviar_mensaje(driver, ["¿Quieres buscar otro movimiento? (Si/No)"])
        resp = recoger_ultimo_mensaje(driver)
        if "Si" not in resp and "si" not in resp:
            flag = False


def mostrar_movimientos(driver: webdriver, correo: str, lista_movimientos):
    mensaje = ["_*Todos los movimientos:*_"]
    for movimiento in lista_movimientos:
        if movimiento.email == correo:
            mensaje.append(movimiento.__str__())

    enviar_mensaje(driver, mensaje)


def get_nombre(correo, lista_movimientos):
    nombre = ""
    for movimiento in lista_movimientos:

        if movimiento.email == correo:
            nombre = movimiento.nombre
    return nombre
