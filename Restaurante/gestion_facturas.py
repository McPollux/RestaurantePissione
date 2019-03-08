# from Restaurante.declaraciones import piss import --- Redundante ya que ya es importando en Restaurante.cargas
from Restaurante.facturas import factura
from Restaurante.cargas import *
from Restaurante.gestion_clientes import validoDNI
import datetime


def abrirFactura(widget):
    """
    Evento que se lanza cuando se pulsa cualquiera de los botones de mesa. Introduce la información basica en la pestaña
    y en caso de que la mesa seleccionada ya tuviera almacenada información(datos del cliente/comandas) previamente, la carga.
    A parte de esto actualiza el color de los botones de acuerdo a la acción realizada.
    """
    piss.lblTotal.set_text("0")
    liberarAzul()
    if widget == piss.btnMesa1:
        piss.mesaAzul = 1
        piss.lblMesa.set_text("1")
        widget.set_image(piss.azulMesa1)
        cargarDatos(1)
    elif widget == piss.btnMesa2:
        piss.mesaAzul = 2
        piss.lblMesa.set_text("2")
        widget.set_image(piss.azulMesa2)
        cargarDatos(2)
    elif widget == piss.btnMesa3:
        piss.mesaAzul = 3
        piss.lblMesa.set_text("3")
        widget.set_image(piss.azulMesa3)
        cargarDatos(3)
    elif widget == piss.btnMesa4:
        piss.mesaAzul = 4
        piss.lblMesa.set_text("4")
        widget.set_image(piss.azulMesa4)
        cargarDatos(4)
    elif widget == piss.btnMesa5:
        piss.mesaAzul = 5
        piss.lblMesa.set_text("5")
        widget.set_image(piss.azulMesa5)
        cargarDatos(5)
    elif widget == piss.btnMesa6:
        piss.mesaAzul = 6
        piss.lblMesa.set_text("6")
        widget.set_image(piss.azulMesa6)
        cargarDatos(6)
    elif widget == piss.btnMesa7:
        piss.mesaAzul = 7
        piss.lblMesa.set_text("7")
        widget.set_image(piss.azulMesa7)
        cargarDatos(7)
    elif widget == piss.btnMesa8:
        piss.mesaAzul = 8
        piss.lblMesa.set_text("8")
        widget.set_image(piss.azulMesa1)
        cargarDatos(8)

    piss.lblCamarero.set_text(piss.camarero)
    now = datetime.datetime.now()
    piss.lblFecha.set_text(str(now.day) + "/" + str(now.month) + "/" + str(now.year))

    piss.gbFactura.show()

    piss.notebook.set_current_page(1)


def liberarAzul():
    """
    Se usa unicamente en el metodo abrirFactura. Recorre todos los botones y en caso de estar alguno en azul lo pone en
    rojo.
    """
    mesaAzul = piss.mesaAzul
    if piss.mesaAzul != -1:
        if mesaAzul == 1:
            piss.btnMesa1.set_image(piss.rojoMesa1)
            return
        if mesaAzul == 2:
            piss.btnMesa2.set_image(piss.rojoMesa2)
            return
        if mesaAzul == 3:
            piss.btnMesa3.set_image(piss.rojoMesa3)
            return
        if mesaAzul == 4:
            piss.btnMesa4.set_image(piss.rojoMesa4)
            return
        if mesaAzul == 5:
            piss.btnMesa5.set_image(piss.rojoMesa5)
            return
        if mesaAzul == 6:
            piss.btnMesa6.set_image(piss.rojoMesa6)
            return
        if mesaAzul == 7:
            piss.btnMesa7.set_image(piss.rojoMesa7)
            return
        if mesaAzul == 8:
            piss.btnMesa8.set_image(piss.rojoMesa8)
            return


def buscarCliente(widget, data2=None):
    """
    Evento que se lanza al salir del entry donde se introduce el DNI del cliente. En caso de que el DNI introducido concuerde
    con alguno ya almacenado en la base de datos, autocompleta el resto de la información.
    """
    piss.booleanCliente = False
    piss.curRestaurante.execute("select * from Clientes")
    clientes = piss.curRestaurante.fetchall()
    for i in clientes:
        if piss.etDni.get_text() == i[0]:
            piss.etNombre.set_text(i[1])
            piss.etApellidos.set_text(i[2])
            piss.etDireccion.set_text(i[3])
            piss.cmbProvincia.set_active(idProvincia(i[4]))
            piss.cmbCiudad.set_active(idCiudad(i[5]))
            piss.booleanCliente = True


def idProvincia(nombre):
    """
    Dado el nombre de una provincia devuelve su id correspondiente en la base de datos.
    """
    piss.curReverb.execute("select id, provincia from provincias")
    provincias = piss.curReverb.fetchall()
    for i in provincias:
        if i[1] == nombre:
            return int(i[0] - 1)


def idCiudad(nombre):
    """
    Dado el nombre de una ciudad devuelve su id correspondiente en la lista.
    """
    cont = 0
    for i in piss.listMunicipios:
        if i[0] == nombre:
            return cont
        cont += 1


def anhadirComanda(widget):
    """
    Evento que se lanza cuando el usuario pulsa en añadir tras elegir algun servicio en la pestaña de factura.
    Cada pulsación individual añade un producto más a la tabla de comandas.
    """
    b = False

    seleccion = piss.treeSelServicios.get_selection()
    (tm, ti) = seleccion.get_selected()
    id = tm.get_value(ti, 0)
    precio = float([tm.get_value(ti, 2)[0:-1]][0])
    piss.lblTotal.set_text("%.2f" % (float(piss.lblTotal.get_text()) + precio))
    listaComandas = piss.listas[int(piss.lblMesa.get_text())]
    for i in range(len(listaComandas)):
        if id == listaComandas[i][0]:
            listaComandas[i][2] += 1
            listaComandas[i][3] = "%.2f" % (precio * listaComandas[i][2]) + "€"
            b = True
            break

    if not b:
        lista = (id, "%.2f" % precio + "€", 1,
                 "%.2f" % precio + "€")  # Precio sacado de la tabla de servicios, extraido el campo "€" y formateado para tener solo 2 decimales
        listaComandas.append(lista)


def eliminarComanda(widget):
    """
    Evento que se lanza cuando el usuario pulsa el boton correspondiente tras elegir alguna comanda en la pestaña de factura.
    Pulsar este botón borra la tupla entera y actualiza el precio de la factura correspondientemente.
    """
    seleccion = piss.treeComandas.get_selection()
    (tm, ti) = seleccion.get_selected()
    if ti is not None:
        precioComanda = float([tm.get_value(ti, 3)[0:-1]][0])
        piss.lblTotal.set_text("%.2f" % (float(piss.lblTotal.get_text()) - precioComanda))
        tm.remove(ti)


def imprimir(widget):
    """
    Evento que se lanza cuando el usuario pulsa en imprimir en la pestaña de factura. En caso de que los campos obligatorios
    esten bien completos guarda la infomación en la base de datos, limpia los campos y libera la mesa.
    """
    piss.lblError.set_text("")

    if piss.etDni.get_text() == "":
        piss.lblError.set_text("El campo de DNI no puede estar vacio")
        return
    if not validoDNI(piss.etDni.get_text()) and  piss.etDni.get_text() != "0":
        piss.lblError.set_text("El campo de DNI no cumple el formato adecuado")
        return

    mesaNum = int(piss.lblMesa.get_text())
    for i in range(len(piss.mesas)):
        if mesaNum != i and piss.etDni.get_text() == piss.mesas[i].dni:
            piss.lblError.set_text("Este cliente ya está ocupando una mesa")
            return

    if piss.etNombre.get_text() == "":
        piss.lblError.set_text("El campo de nombre no puede estar vacio")
        return

    if piss.cmbProvincia.get_active() == -1:
        piss.lblError.set_text("El campo de provincia no puede estar vacio")
        return

    if piss.cmbCiudad.get_active() == -1:
        piss.lblError.set_text("El campo de ciudad no puede estar vacio")
        return

    if not piss.booleanCliente:
        altaClienteFac()

    altaFactura()
    vaciarFactura()
    liberarMesa()
    piss.notebook.set_current_page(0)
    piss.gbFactura.hide()


def liberarMesa():
    """
    Parte del evento imprimir. Metodo que libera la mesa en la que se ha facturado y cambia el color de su correspondiente botón.
    """
    mesaLiberar = int(piss.lblMesa.get_text())
    if mesaLiberar == 1:
        piss.btnMesa1.set_image(piss.verdeMesa1)
        return
    if mesaLiberar == 2:
        piss.btnMesa2.set_image(piss.verdeMesa2)
        return
    if mesaLiberar == 3:
        piss.btnMesa3.set_image(piss.verdeMesa3)
        return
    if mesaLiberar == 4:
        piss.btnMesa4.set_image(piss.verdeMesa4)
        return
    if mesaLiberar == 5:
        piss.btnMesa5.set_image(piss.verdeMesa5)
        return
    if mesaLiberar == 6:
        piss.btnMesa6.set_image(piss.verdeMesa6)
        return
    if mesaLiberar == 7:
        piss.btnMesa7.set_image(piss.verdeMesa7)
        return
    if mesaLiberar == 8:
        piss.btnMesa8.set_image(piss.verdeMesa8)
        return


def altaFactura():
    """
    Parte del evento imprimir. Metodo que da de alta en la base de datos tanto las comandas como la propia factura y
    llama al metodo factura que genera una version PDF A6 para su impresión.
    """
    piss.curRestaurante.execute("select idCamarero from camareros where nombre = '" + piss.camarero + "'")
    idCamarero = piss.curRestaurante.fetchall()

    lista = (piss.etDni.get_text(), idCamarero[0][0], int(piss.lblMesa.get_text()), datetime.datetime.now(),
             float(piss.lblTotal.get_text()))

    piss.curRestaurante.execute(
        "insert into facturas (dni, idCamarero, idMesa, fecha, total) values (?, ?, ?, ?, ?)", lista)
    piss.conexPissione.commit()
    cargarFacturas()

    # Ahora cogemos la factura de la base de datos
    piss.curRestaurante.execute("select max(idFactura) from facturas")
    id = piss.curRestaurante.fetchall()

    for i in piss.treeComandas.get_model():
        piss.curRestaurante.execute("insert into lineasFactura (idFactura, idServicio, cantidad) values (?, ?, ?)",
                                    (id[0][0], i[0], i[2]))

    piss.conexPissione.commit()

    factura(id[0][0])
    piss.lblError.set_text("")
    piss.lblTotal.set_text("0")
    piss.treeComandas.get_model().clear()


def vaciarFactura():
    """
    Limpia todos los campos del cliente.
    """
    piss.etDni.set_text("")
    piss.etDireccion.set_text("")
    piss.etNombre.set_text("")
    piss.etApellidos.set_text("")
    piss.cmbProvincia.set_active(-1)
    piss.cmbCiudad.set_active(-1)


def altaClienteFac():
    """
    Parte del evento imprimir. Este metodo solo se lanza en caso de que el cliente introducido no esté ya almacenado en la base de datos.
    Tomando la informacion necesaria da de alta un nuevo cliente.
    """
    tree_prov = piss.cmbProvincia.get_active_iter()
    tree_local = piss.cmbCiudad.get_active_iter()
    model = piss.cmbProvincia.get_model()
    prov = model[tree_prov][0]
    model = piss.cmbCiudad.get_model()
    localidad = model[tree_local][0]

    lista = (
        piss.etDni.get_text(), piss.etNombre.get_text(), piss.etApellidos.get_text(), piss.etDireccion.get_text(),
        prov,
        localidad)
    piss.curRestaurante.execute("insert into clientes values (?, ?, ?, ?, ?, ?)", lista)
    piss.conexPissione.commit()


def bajaFactura(widget):
    """
    Evento que se lanza cuando el usuario pulsa el botón correspondiente para borrar la factura de la base de datos.
    Este botón esta disponible ya que simulamos que las facturas almacenadas en la base de datos son tickets previos a
    la factura.
    """
    a = piss.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    piss.curRestaurante.execute("delete from facturas where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
    piss.conexPissione.commit()

    piss.listLineasFactura.clear()
    cargarFacturas()


def visualizarComandas(widget):  #
    """
    Metodo que se lanza al clicar en una tupla de la tabla de gestion de facturas. Visualiza la informacion de sus comandas
    en la tabla inferior.
    """
    piss.listLineasFactura.clear()
    a = piss.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    if ti is not None:
        piss.curRestaurante.execute(
            "select * from LineasFactura where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
        lineasFactura = piss.curRestaurante.fetchall()

        for i in lineasFactura:
            piss.curRestaurante.execute("select nombre, precio from servicios where idServicio = \'" + str(i[2]) + "\'")
            nombrePrecio = piss.curRestaurante.fetchall()
            piss.listLineasFactura.append((i[0], i[3], nombrePrecio[0][0], "%.2f" % (nombrePrecio[0][1] * i[3]) + "€"))

        piss.etIdFactura.set_text(str(tm.get_value(ti, 0)))
        piss.etDni2.set_text(str(tm.get_value(ti, 1)))
        piss.etFecha.set_text(str(tm.get_value(ti, 4)))


def guardarDatos():
    """
     Metodo llamado desde verificarCambio, de "restaurante.py". Guarda los datos de la mesa actual en su correspondiente
     objeto.
    """
    posicion = int(piss.lblMesa.get_text())
    piss.mesas[posicion].dni = piss.etDni.get_text()
    piss.mesas[posicion].nombre = piss.etNombre.get_text()
    piss.mesas[posicion].apellidos = piss.etApellidos.get_text()
    piss.mesas[posicion].direccion = piss.etDireccion.get_text()
    piss.mesas[posicion].provincia = piss.cmbProvincia.get_active()
    piss.mesas[posicion].ciudad = piss.cmbCiudad.get_active()
    piss.mesas[posicion].total = piss.lblTotal.get_text()

    vaciarFactura()


def printPDF(widget):
    """
     Evento que se lanza cuando el usuario pulsa imprimir en una factura desde el gestor de facturas, genera y visualiza la información
     en formato PDF.
    """
    a = piss.treeFacturas.get_selection()
    (tm, ti) = a.get_selected()
    factura(tm.get_value(ti, 0))


def desSelect(widget):
    """
     Evento que se lanza al clicar cualquier tupla de la tabla de comandas en el gesto de facturas, su unico proposito es
     cancelar la selección por motivos puramente estéticos.
    """
    piss.treeNoFuncional.unselect_all()

# EOF
