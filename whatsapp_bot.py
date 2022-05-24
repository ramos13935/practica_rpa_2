import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

"""
AAntes de empezar debes abrir la powershell e ir a la carpeta dónde esté instalado chrome
 cd C:\"Program Files"\Google\Chrome\Application
Después hay que ejecutar chrome con este comando
 .\chrome.exe --remote-debugging-port=9999 --user-data-dir="C:\test"

"""


def start(lista_incidencias):
    apagar = False

    driver = abrir_navegador()
    while not apagar:
        abrir_chat(driver, "Reposo")
        abrir_primer_chat_no_leido(driver)

        nombre, tlf = saber_nombre(driver, lista_incidencias)
        saludar(driver, nombre)
        salir = False
        # correo = esperar_correo(driver)
        while not salir:
            salir = menu(driver, tlf, lista_incidencias)

        mensaje_despedida = "¡Nos vemos pronto!"
        enviar_mensaje(driver, [mensaje_despedida])


def menu(driver: webdriver, tlf, lista_incidencias):
    # nombre = "Bienvenido/a " + get_nombre(correo, lista_incidencias) + " las opciones disponibles son:"
    # nombre = saber_nombre(driver, lista_incidencias)

    opciones = "Las opciones disponibles son:"
    op1 = "*1.* Incidencias"
    op2 = "*2.* Peticiones"
    op3 = "*3.* Hablar con un agente"
    op0 = "*0.* Finalizar"
    enviar_mensaje(driver, [opciones, op1, op2, op3, op0])
    opcion = recoger_ultimo_mensaje(driver)
    if opcion == "1":
        submenu_incidencias(driver, tlf, lista_incidencias)
        return False
    elif opcion == "2":
        enviar_mensaje(driver, ["Característica no desarrollada"])
        return False

    elif opcion == "3":
        enviar_mensaje(driver, ["Puede llamar al 12345679 (L-V, 8:00-21:00) para obtener más información"])
        return True
    elif opcion == "0":
        return True
    else:
        enviar_mensaje(driver, ["Por favor escriba una de las opciones válidas"])
        return False



def submenu_incidencias(driver, tlf, lista_incidencias):
    tit = "*INCIDENCIAS*"
    op1 = "*1.* Buscar incidencia"
    op2 = "*2.* Mostrar incidencias "
    op0 = "*0.* Volver al menú principal"
    flag = True
    while flag:
        enviar_mensaje(driver, [tit, op1, op2, op0])
        resp = recoger_ultimo_mensaje(driver)
        if resp == "1":
            mostrar_incidencia(driver, tlf, lista_incidencias)
        elif resp == "2":
            mostrar_incidencias(driver, tlf, lista_incidencias)
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


def abrir_primer_chat_no_leido(driver: webdriver):
    encontrado = False
    while not encontrado:
        try:
            chats = driver.find_elements(by=By.XPATH,
                                         value='//span[@class = "l7jjieqr cfzgl7ar ei5e7seu h0viaqh7 tpmajp1w c0uhu3dl riy2oczp dsh4tgtl sy6s5v3r gz7w46tb lyutrhe2 qfejxiq4 fewfhwl7 ovhn1urg ap18qm3b ikwl5qvt j90th5db aumms1qt"]')
            chats[0].click()
            encontrado = True
            time.sleep(2)
        except IndexError as e:
            pass


def esperar_correo(driver: webdriver):
    flag = True
    correo = ""
    while flag:
        correo = recoger_ultimo_mensaje(driver)
        if "@" in correo:
            flag = False
        else:
            enviar_mensaje(driver, ["Escribe un *correo electrónico* válido por favor."])

    return correo


def saludar(driver: webdriver, nombre):
    saludo = "Bienvenido/a " + nombre + " , soy Jarvis, tu asistente."
    em = ":saludar"
    enviar_mensaje(driver, [saludo, em])


def recoger_ultimo_mensaje(driver: webdriver):
    check = False
    ultimo_mensaje = ""
    value_mensajes = '//*[@id="main"]/div[3]/div/div[2]/div/div/div/div/div/div/div/span[@class="i0jNr selectable-text copyable-text"]/span'
    # value_mensajes = '//*[@id="main"]/div[3]/div/div[2]/div/div[contains(@class, "message-i")]/div/div/div/div/div/span[@class="i0jNr selectable-text copyable-text"]/span'
    contador_mesajes = len(driver.find_elements(by=By.XPATH, value=value_mensajes))
    while not check:
        mensajes_usu = driver.find_elements(by=By.XPATH,
                                            value=value_mensajes)

        if len(mensajes_usu) > contador_mesajes:
            ultimo_mensaje = mensajes_usu[-1].text
            check = True

        # time.sleep(0.5)
    return ultimo_mensaje


def mostrar_incidencia(driver: webdriver, tlf: str, lista_incidencias: list):
    flag = True
    while flag:
        enviar_mensaje(driver, ["Escribe el código del incidencia que quieres revisar:"])
        cod_mov = recoger_ultimo_mensaje(driver)
        mensaje = ["_*Datos del incidencia:*_"]
        permiso = True
        for incidencia in lista_incidencias:
            if str(incidencia.codigo_incidencia) == cod_mov and incidencia.telefono in tlf:
                mensaje.append(incidencia.__str__())
                break
            elif str(incidencia.codigo_incidencia) == cod_mov and incidencia.telefono not in tlf:
                enviar_mensaje(driver, ["No tienes permiso para ver ese incidencia"])
                permiso = False
                break

        if permiso and len(mensaje) > 1:
            enviar_mensaje(driver, mensaje)
        elif permiso:
            enviar_mensaje(driver, ["Código de incidencia no encontrado"])

        enviar_mensaje(driver, ["¿Quieres buscar otro incidencia? (Si/No)"])
        resp = recoger_ultimo_mensaje(driver)
        if "Si" not in resp and "si" not in resp and "Sí" not in resp and "SÍ" not in resp:
            flag = False


def mostrar_incidencias(driver: webdriver, tlf: str, lista_incidencias):
    mensaje = ["_*Todos los movimientos:*_"]
    for incidencia in lista_incidencias:
        if incidencia.telefono in tlf:
            mensaje.append(incidencia.__str__())

    enviar_mensaje(driver, mensaje)


def saber_nombre(driver: webdriver, lista_incidencias: list):
    # Conseguir telefono chat
    tlf = driver.find_element(by=By.XPATH,
                              value='//div[@class="_21nHd"]/span[@class = "ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr"]').text
    tlf = tlf.replace(" ", "")
    return get_nombre(tlf, lista_incidencias), tlf


def get_nombre(tlf: str, lista_incidencias: list):
    nombre = ""
    for incidencia in lista_incidencias:
        if incidencia.telefono in tlf:
            nombre = incidencia.nombre
            break
    return nombre
