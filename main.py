import time
from movimiento import Movimiento
import whatsapp_bot

import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

workbook = openpyxl.load_workbook("movimientos.xlsx")
sheet = workbook.active
a1 = sheet['A1']
filas = sheet
lista_movimientos = []

for fila in filas.iter_rows(min_row=2):
    email = fila[0].value
    nom = fila[1].value
    apell = fila[2].value
    cod_oper = fila[3].value
    nombre_oper = fila[4].value
    estado_oper = fila[5].value

    lista_movimientos.append(Movimiento(nom, apell, email, cod_oper, nombre_oper, estado_oper))

workbook.close()
# FIN DEL EXCEL #
# INICO BOT WAHTSAPP #
whatsapp_bot.start(lista_movimientos)
