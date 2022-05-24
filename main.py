from incidencia import Incidencia
import whatsapp_bot
import openpyxl

workbook = openpyxl.load_workbook("incidencias.xlsx")
sheet = workbook.active
a1 = sheet['A1']
filas = sheet
lista_incidencias = []

for fila in filas.iter_rows(min_row=2):
    email = fila[0].value
    nom = fila[1].value
    apell = fila[2].value
    tlf = fila[3].value
    cod_oper = fila[4].value
    nombre_oper = fila[5].value
    estado_oper = fila[6].value

    lista_incidencias.append(Incidencia(nom, apell, email, tlf, cod_oper, nombre_oper, estado_oper))

workbook.close()
# FIN DEL EXCEL #
# INICO BOT WAHTSAPP #
whatsapp_bot.start(lista_incidencias)
