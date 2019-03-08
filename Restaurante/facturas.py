from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
import os
from Restaurante.restaurante import piss

""" Modulo generardor de documentos

"""


def cabecera(cser):
    """ Crea la cabecera del documento

        Esta cabecera mostrara los datos principales de la empresa
        que se repetirá en todos los documentos

    """
    try:
        cser.setTitle('Factura')
        cser.setAuthor('Pissione')
        cser.setFont('Helvetica', size=11)
        cser.line(25, 390, 275, 390)
        textnom = 'RESTAURANTE PISSIONE'
        textdir = 'Avenida Galicia, 102 - Vigo'
        texttlfo = '886 20 21 22'
        cser.drawString(80, 370, textnom)
        cser.line(25, 355, 275, 355)
        cser.drawString(140, 335, textdir)
        cser.drawString(208, 320, texttlfo)
    except:
        print ('Error de cabecera')


def pie(cser):
    """ Crea el pie del documento

        El pie mostrará el agradecimiento al cliente
        y la fecha de creación del documento y nº de pagina si fuese necesario

    """
    try:
        cser.line(25, 20, 275, 20)
        textgracias = "Gracias por su visita"
        cser.drawString(175, 10, textgracias)

    except:
        print('Error de pie')


def factura(idfactura):

    """ Crea la factura para el cliente

        Este documento crea la factura. Necesita acceder a dos tablas (join), la propia de la factura y
        la tabla de servicio para obtener los nombres de las comandas y precios y asi generar
        los totales y subtotales. Hay ajustes para una mejor alineacion de la presentacion

    """

    cser = canvas.Canvas('servicios.pdf', pagesize=A6)
    cser.setDash(7, 2)
    cabecera(cser)
    pie(cser)
    piss.curRestaurante.execute(
        'select cantidad, s.nombre, s.precio, c.nombre, cl.dni, cl.nombre from LineasFactura lf, servicios s, facturas f, camareros c, clientes cl where f.idFactura = ? and lf.idFactura = f.idFactura and s.idServicio = lf.idServicio and f.idcamarero = c.idCamarero and cl.dni= f.dni',
        (idfactura,))
    listado = piss.curRestaurante.fetchall()

    piss.conexPissione.commit()
    textlistado = 'Factura'
    cser.drawString(25, 395, textlistado)
    cser.line(25, 700, 525, 700)
    x = 25
    y = 240
    total = 0
    if listado[0][4] != "0":        #En caso de ser un cliente anonimo no se visualiza el campo DNI
        cser.drawString(25, 300, "Cliente: " + listado[0][5])
        cser.drawString(25, 285, "DNI: " + listado[0][4])
    else:
        cser.drawString(25, 285, "Cliente: " + listado[0][5])
    cser.drawString(25, 270, "Ha sido atendido por: "+listado[0][3])
    cser.line(25, 260, 275, 260)
    cser.drawString(x, y, "Uds.")
    x = x + 25
    cser.drawString(x, y, "Nombre del servicio")
    x = x + 110
    cser.drawString(x, y, "Precio Ud.")
    x = x + 70
    cser.drawString(x, y, "Subtotal")
    cser.line(25, 230, 275, 230)
    x = 25
    y = y - 30

    for registro in listado:
        for i in range(3):
            if i <= 1:
                cser.drawString(x, y, str(registro[i]))
                x = x + 25
            elif i == 2:
                x = x + 90
                cser.drawString(x, y, ("%.2f" % registro[i]) + "€")

            var1 = int(registro[0])

            var2 = round(float(registro[2]), 2)
            subtotal = var1 * var2

        total = total + subtotal
        subtotal = ("%.2f" % subtotal) + "€"
        x = x + 70
        cser.drawString(x, y, str(subtotal))
        y = y - 20
        x = 25

    y = y - 20
    cser.line(25, y, 275, y)
    y = y - 20
    x = 210
    cser.drawString(x, y, 'Total:')
    x = 240
    total = ("%.2f" % total) + "€"
    cser.drawString(x, y, str(total))
    try:
        cser.showPage()
        cser.save()
        dir = os.getcwd()
        os.system('/usr/bin/xdg-open ' + dir + '/servicios.pdf')
    except Exception as e:
        print(e)