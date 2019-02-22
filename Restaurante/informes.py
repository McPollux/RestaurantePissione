from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
import os
import locale
import sqlite3


""" Modulo generardor de documentos

"""


cser = canvas.Canvas('servicios.pdf', pagesize=A6)


def cabecera():
    """ Crea la cabecera del documento

        Esta cabecera mostrara los datos principales de la empresa
        que se repetirá en todos los documentos

    """
    try:


        cser.setTitle('Informes')
        cser.setAuthor('Pissione')
        cser.setFont('Helvetica', size=11)
        cser.line(50, 820, 525, 820)
        cser.line(50, 745, 525, 745)
        textnom = 'RESTAURANTE PISSIONE'
        textdir = 'Avenida Galicia, 102 - Vigo'
        texttlfo = '886 20 21 2'
        cser.drawString(255, 795, textnom)
        cser.drawString(245, 775, textdir)
        cser.drawString(280, 755, texttlfo)
    except:
        print ('erros cabecera')

def pie():
    """ Crea el pie del documento

        El pie mostrará el agradecimiento al cliente
        y la fecha de creación del documento y nº de pagina si fuese necesario

    """
    try:
        cser.line(50, 20, 525, 20)
        textgracias = "Gracias por su visita"
        cser.drawString(220, 10, textgracias)

    except:
        print('erros pie')


def factura(idfactura):

    """ Crea la factura para el cliente

        Este documento crea la factura. Necesita acceder a dos tablas (join), la propia de la factura y
        la tabla de servicio para obtener los nombres de las comandas y precios y asi generar
        los totales y subtotales. Hay ajustes para una mejor alineacion de la presentacion

    """

    try:
        bbdd = 'pissione.sqlite'  # variable almacena base de datos
        conexPissione = sqlite3.connect(bbdd)
        curRestaurante = conexPissione.cursor()
        curRestaurante.execute("PRAGMA foreign_keys = ON")
        conexPissione.commit()
    # le conectamos el cursor
    except sqlite3.OperationalError as e:
        print(e)

    cabecera()
    pie()
    curRestaurante.execute(
        'select idComanda, s.nombre, cantidad, s.precio from LineasFactura lf, servicios s where lf.idFactura = ? and s.idServicio = lf.idServicio',
        (idfactura,))
    listado = curRestaurante.fetchall()
    print(len(listado))

    conexPissione.commit()
    textlistado = 'Factura'
    cser.drawString(255, 705, textlistado)
    cser.line(50, 700, 525, 700)
    x = 50
    y = 680
    total = 0
    for registro in listado:
        for i in range(4):
            if i <= 1:
                cser.drawString(x, y, str(registro[i]))
                x = x + 40
            else:
                x = x + 120
                cser.drawString(x, y, str(registro[i]))
            print(registro[0])
            print(registro[1])
            print(registro[2])
            var1 = int(registro[2])
            print(registro[3])
            var2 = round(float(registro[3]), 2)
            subtotal = var1 * var2
        total = total + subtotal
        subtotal = locale.currency(subtotal)
        x = x + 120
        cser.drawString(x, y, str(subtotal))
        y = y - 20
        x = 50
    y = y - 20
    cser.line(50, y, 525, y)
    y = y - 20
    x = 400
    cser.drawString(x, y, 'Total: ')
    x = 485
    total = round(float(total), 2)
    total = locale.currency(total)
    print(total)
    cser.drawString(x, y, str(total))
    cser.showPage()
    cser.save()
    dir = os.getcwd()
    os.system('/usr/bin/xdg-open ' + dir + '/servicios.pdf')
