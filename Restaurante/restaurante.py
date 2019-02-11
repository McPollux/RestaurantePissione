import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import datetime
import sqlite3


class Mesas:

    def __init__(self, dni="", nombre="", apellidos="", direccion="", provincia=-1, ciudad=-1,
                 total=0):
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos
        self.direccion = direccion
        self.provincia = provincia
        self.ciudad = ciudad
        self.total = total


class Hola:

    def __init__(self):
        # Iniciamos la libreria GTK
        b = Gtk.Builder()
        b.add_from_file('Restaurante.glade')

        try:
            self.bbdd = 'pissione.sqlite'  # variable almacena base de datos
            self.conexPissione = sqlite3.connect(self.bbdd)
            self.curRestaurante = self.conexPissione.cursor()
            self.curRestaurante.execute("PRAGMA foreign_keys = ON")
            self.conexPissione.commit()
        # le conectamos el cursor
        except sqlite3.OperationalError as e:
            print(e)

        try:
            self.reverb = 'act17.sqlite'  # variable almacena base de datos
            self.conexReverb = sqlite3.connect(self.reverb)
            self.curReverb = self.conexReverb.cursor()
        # le conectamos el cursor
        except sqlite3.OperationalError as e:
            print(e)

        self.notebook = b.get_object("notebook")

        # Mesas
        self.venprincipal = b.get_object("PriWin")
        self.btnMesa1 = b.get_object("btnMesa1")
        self.btnMesa2 = b.get_object("btnMesa2")
        self.btnMesa3 = b.get_object("btnMesa3")
        self.btnMesa4 = b.get_object("btnMesa4")
        self.btnMesa5 = b.get_object("btnMesa5")
        self.btnMesa6 = b.get_object("btnMesa6")
        self.btnMesa7 = b.get_object("btnMesa7")
        self.btnMesa8 = b.get_object("btnMesa8")

        self.listComandas1 = b.get_object("listComandas1")
        self.listComandas2 = b.get_object("listComandas2")
        self.listComandas3 = b.get_object("listComandas3")
        self.listComandas4 = b.get_object("listComandas4")
        self.listComandas5 = b.get_object("listComandas5")
        self.listComandas6 = b.get_object("listComandas6")
        self.listComandas7 = b.get_object("listComandas7")
        self.listComandas8 = b.get_object("listComandas8")

        self.listas = (
            self.listComandas1, self.listComandas2, self.listComandas3, self.listComandas4, self.listComandas5,
            self.listComandas6, self.listComandas7, self.listComandas8)

        self.mesas = (
            Mesas(), Mesas(), Mesas(), Mesas(),
            Mesas(), Mesas(), Mesas(), Mesas())

        # Facturas
        self.listProvincias = b.get_object("listProvincias")
        self.listMunicipios = b.get_object("listMunicipios")
        self.listSelServicios = b.get_object("listSelServicios")
        self.gbFactura = b.get_object("gbFactura")
        self.lblMesa = b.get_object("lblMesa")
        self.lblCamarero = b.get_object("lblCamarero")
        self.lblFecha = b.get_object("lblFecha")
        self.etDni = b.get_object("etDni")
        self.etNombre = b.get_object("etNombre")
        self.etApellidos = b.get_object("etApellidos")
        self.etDireccion = b.get_object("etDireccion")
        self.cmbProvincia = b.get_object("cmbProvincia")
        self.cmbCiudad = b.get_object("cmbCiudad")
        self.treeComandas = b.get_object("treeComandas")
        self.treeSelServicios = b.get_object("treeSelServicios")
        self.lblTotal = b.get_object("lblTotal")
        self.lblError = b.get_object("lblError")
        self.booleanCliente = False

        # Administracion
        self.treeFacturas = b.get_object("treeFacturas")
        self.treeLineasFactura = b.get_object("treeLineasFactura")
        self.listLineasFactura = b.get_object("listLineasFactura")

        self.listFacturas = b.get_object("listFacturas")
        self.listClientes = b.get_object("listClientes")
        self.listCamareros = b.get_object("listCamareros")
        self.listMesas = b.get_object("listMesas")

        self.etIdFactura = b.get_object("etIdFactura")
        self.cmbMesas = b.get_object("cmbMesas")
        self.etDni2 = b.get_object("etDni2")
        self.etFecha = b.get_object("etFecha")
        self.cmbCamareros = b.get_object("cmbCamareros")
        self.cbCompletado = b.get_object("cbCompletado")

        self.treeServicios = b.get_object("treeServicios")
        self.treeSelServicio = b.get_object("treeSelServicio")
        self.etNomServ = b.get_object("etNomServ")
        self.etPrecioUniServ = b.get_object("etPrecioUniServ")

        dic = {'on_PriWin_destroy': self.salir,
               'on_notebook_switch_page': self.verificarCambio,
               'on_btnMesa1_clicked': self.abrirFactura,
               'on_btnMesa2_clicked': self.abrirFactura,
               'on_btnMesa3_clicked': self.abrirFactura,
               'on_btnMesa4_clicked': self.abrirFactura,
               'on_btnMesa5_clicked': self.abrirFactura,
               'on_btnMesa6_clicked': self.abrirFactura,
               'on_btnMesa7_clicked': self.abrirFactura,
               'on_btnMesa8_clicked': self.abrirFactura,
               'on_etDni_focus_out_event': self.buscarCliente,
               'on_cmbProvincia_changed': self.cargarMunicipios,
               'on_btnAnhadir_clicked': self.anhadirComanda,
               'on_btnEliminarComanda_clicked': self.eliminarComanda,
               'on_btnImprimir_clicked': self.imprimir,
               'on_btnBajaFac_clicked': self.bajaFactura,
               'on_btnAltaServicio_clicked': self.altaServicio,
               'on_btnBajaServicio_clicked': self.bajaServicio,
               'on_treeSelClientes_changed': self.visualizarCliente,
               'on_treeSelFacturas_changed': self.visualizarComandas,
               'on_treeSelServicio_changed': self.visualizarServicio,
               'on_mbSalir_activate': self.salir,
               }

        b.connect_signals(dic)
        self.gbFactura.hide()
        self.cargarServicios()
        self.cargarFacturas()
        self.cargarClientes()
        self.cargarCamareros()
        self.cargarMesas()
        self.venprincipal.show()

    def verificarCambio(self, widget, redundancia, paginaPosterior):
        if paginaPosterior == 1 and self.lblMesa.get_text() == "NULL":
            self.gbFactura.hide()
        if self.notebook.get_current_page() == 1:
            self.guardarDatos()

    def cargarServicios(self):
        self.curRestaurante.execute("select * from Servicios")
        lista = self.curRestaurante.fetchall()
        self.listSelServicios.clear()
        for i in lista:
            i = (i[0], i[1], str("%.2f" % i[2]) + "€")
            self.listSelServicios.append(i)

    def cargarCamareros(self):
        self.curRestaurante.execute("select idCamarero from Camareros")
        lista = self.curRestaurante.fetchall()
        self.listCamareros.clear()
        for i in lista:
            self.listCamareros.append(i)

    def cargarMesas(self):
        self.curRestaurante.execute("select idMesa from Mesas")
        lista = self.curRestaurante.fetchall()
        self.listMesas.clear()
        for i in lista:
            self.listMesas.append(i)


    def cargarDatos(self, posicion):
        self.treeComandas.set_model(self.listas[posicion])
        self.treeComandas.show()
        self.etDni.set_text(self.mesas[posicion].dni)
        self.etNombre.set_text(self.mesas[posicion].nombre)
        self.etApellidos.set_text(self.mesas[posicion].apellidos)
        self.etDireccion.set_text(self.mesas[posicion].direccion)
        self.cmbProvincia.set_active(self.mesas[posicion].provincia)
        self.cmbCiudad.set_active(self.mesas[posicion].ciudad)
        self.lblTotal.set_text(str(self.mesas[posicion].total))

    def guardarDatos(self):
        posicion = int(self.lblMesa.get_text())
        self.mesas[posicion].dni = self.etDni.get_text()
        self.mesas[posicion].nombre = self.etNombre.get_text()
        self.mesas[posicion].apellidos = self.etApellidos.get_text()
        self.mesas[posicion].direccion = self.etDireccion.get_text()
        self.mesas[posicion].provincia = self.cmbProvincia.get_active()
        self.mesas[posicion].ciudad = self.cmbCiudad.get_active()
        self.mesas[posicion].total = self.lblTotal.get_text()

        self.vaciarFactura()

    def abrirFactura(self, widget):

        self.cargarProvincias()
        self.lblTotal.set_text("0")
        if widget == self.btnMesa1:
            self.lblMesa.set_text("1")
            self.cargarDatos(1)
        elif widget == self.btnMesa2:
            self.lblMesa.set_text("2")
            self.cargarDatos(2)
        elif widget == self.btnMesa3:
            self.lblMesa.set_text("3")
            self.cargarDatos(3)
        elif widget == self.btnMesa4:
            self.lblMesa.set_text("4")
            self.cargarDatos(4)
        elif widget == self.btnMesa5:
            self.lblMesa.set_text("5")
            self.cargarDatos(5)
        elif widget == self.btnMesa6:
            self.lblMesa.set_text("6")
            self.cargarDatos(6)
        elif widget == self.btnMesa7:
            self.lblMesa.set_text("7")
            self.cargarDatos(7)
        elif widget == self.btnMesa8:
            self.lblMesa.set_text("8")
            self.cargarDatos(8)

        self.lblCamarero.set_text("Jordi Auxiliar")
        now = datetime.datetime.now()
        self.lblFecha.set_text(str(now.day) + "/" + str(now.month) + "/" + str(now.year))

        self.gbFactura.show()

        self.notebook.set_current_page(1)

    def buscarCliente(self, widget, data=None):
        self.booleanCliente = False
        self.curRestaurante.execute("select * from Clientes")
        clientes = self.curRestaurante.fetchall()
        for i in clientes:
            if self.etDni.get_text() == i[0]:
                self.etNombre.set_text(i[1])
                self.etApellidos.set_text(i[2])
                self.etDireccion.set_text(i[3])
                self.cmbProvincia.set_active(self.idProvincia(i[4]))
                self.cmbCiudad.set_active(self.idCiudad(i[5]))
                self.booleanCliente = True

    def idProvincia(self, nombre):
        self.curReverb.execute("select id, provincia from provincias")
        provincias = self.curReverb.fetchall()
        for i in provincias:
            if i[1] == nombre:
                return int(i[0] -1)

    def idCiudad(self, nombre):
        cont = 0
        for i in self.listMunicipios:
            if i[0] == nombre:
                return cont
            cont += 1

    def cargarProvincias(self):

        try:
            self.listProvincias.clear()
            self.curReverb.execute("select provincia from provincias")
            provincias = self.curReverb.fetchall()
            for i in provincias:
                self.listProvincias.append(i)
        except sqlite3.OperationalError as e:
            print(e)

    def cargarMunicipios(self, widget):
        self.listMunicipios.clear()
        self.curReverb.execute(
            "select municipio from municipios where provincia_id = " + str(self.cmbProvincia.get_active() + 1) + "")
        municipios = self.curReverb.fetchall()
        for i in municipios:
            self.listMunicipios.append(i)

    def cargarFacturas(self):
        self.listFacturas.clear()
        self.curRestaurante.execute("select * from Facturas")
        facturas = self.curRestaurante.fetchall()
        for i in facturas:
            self.listFacturas.append((i[0], i[1], i[2], i[3], i[4], i[5], "%.2f" % i[6] + "€"));

    def cargarClientes(self):
        self.listClientes.clear()
        self.curRestaurante.execute("select * from Clientes")
        clientes = self.curRestaurante.fetchall()
        for i in clientes:
            self.listClientes.append(i)

    def anhadirComanda(self, widget):
        b = False

        seleccion = self.treeSelServicios.get_selection()
        (tm, ti) = seleccion.get_selected()
        id = tm.get_value(ti, 0)
        precio = float([tm.get_value(ti, 2)[0:-1]][0])
        self.lblTotal.set_text("%.2f" % (float(self.lblTotal.get_text()) + precio))
        listaComandas = self.listas[int(self.lblMesa.get_text())]
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

    def eliminarComanda(self, widget):

        seleccion = self.treeComandas.get_selection()
        (tm, ti) = seleccion.get_selected()
        if ti is not None:
            precioComanda = float([tm.get_value(ti, 3)[0:-1]][0])
            self.lblTotal.set_text("%.2f" % (float(self.lblTotal.get_text()) - precioComanda))
            tm.remove(ti)

    def imprimir(self, widget):
        self.lblError.set_text("")
        if self.etDni.get_text() != "":
            if self.etNombre.get_text() != "":
                if self.cmbProvincia.get_active() != -1:
                    if self.cmbCiudad.get_active() != -1:
                        if not self.booleanCliente:
                            self.altaCliente()

                        self.altaFactura()
                        self.vaciarFactura()
                        self.notebook.set_current_page(0)
                        self.gbFactura.hide()
                    else:
                        self.lblError.set_text("El campo de ciudad no puede estar vacio")
                else:
                    self.lblError.set_text("El campo de provincia no puede estar vacio")
            else:
                self.lblError.set_text("El campo de nombre no puede estar vacio")
        else:
            self.lblError.set_text("El campo de DNI no puede estar vacio")

    def altaCliente(self):
        tree_prov = self.cmbProvincia.get_active_iter()
        tree_local = self.cmbCiudad.get_active_iter()
        model = self.cmbProvincia.get_model()
        prov = model[tree_prov][0]
        model = self.cmbCiudad.get_model()
        localidad = model[tree_local][0]

        lista = (
            self.etDni.get_text(), self.etNombre.get_text(), self.etApellidos.get_text(), self.etDireccion.get_text(),
            prov,
            localidad)
        self.curRestaurante.execute("insert into clientes values (?, ?, ?, ?, ?, ?)", lista)
        self.conexPissione.commit()

    def altaFactura(self):

        lista = (self.etDni.get_text(), 1, int(self.lblMesa.get_text()), datetime.datetime.now(),
                 float(self.lblTotal.get_text()))

        self.curRestaurante.execute(
            "insert into facturas (dni, idCamarero, idMesa, fecha, total) values (?, ?, ?, ?, ?)", lista)
        self.conexPissione.commit()
        self.cargarFacturas()

        # Ahora cogemos la factura de la base de datos
        self.curRestaurante.execute("select max(idFactura) from facturas")
        id = self.curRestaurante.fetchall()

        for i in self.treeComandas.get_model():
            self.curRestaurante.execute("insert into lineasFactura (idFactura, idServicio, cantidad) values (?, ?, ?)",
                                        (id[0][0], i[0], i[2]))

        self.conexPissione.commit()

        self.lblError.set_text("")
        self.lblTotal.set_text("0")
        self.treeComandas.get_model().clear()

    def bajaFactura(self, widget):
        a = self.treeFacturas.get_selection()
        (tm, ti) = a.get_selected()
        self.curRestaurante.execute("delete from facturas where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
        self.conexPissione.commit()

        self.listLineasFactura.clear()
        self.cargarFacturas()

    def altaServicio(self, widget):

        lista = (self.etNomServ.get_text(), self.etPrecioUniServ.get_text())

        self.curRestaurante.execute("insert into servicios (nombre, precio) values (?, ?)", lista)
        self.conexPissione.commit()
        self.cargarServicios()


    def bajaServicio(self, widget):
        a = self.treeServicios.get_selection()
        (tm, ti) = a.get_selected()
        #Falta codificar que no debe poder borrar ningun servicio ya utilizado en alguna linea de factura
        self.curRestaurante.execute("delete from servicios where idServicio = \'" + str(tm.get_value(ti, 0)) + "\'")
        self.conexPissione.commit()

        self.cargarServicios()

    def vaciarFactura(self):
        self.etDni.set_text("")
        self.etDireccion.set_text("")
        self.etNombre.set_text("")
        self.etApellidos.set_text("")
        self.cmbProvincia.set_active(-1)
        self.cmbCiudad.set_active(-1)

    def validoDNI(self, dni):

        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"  # letras del dni
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            # tabla letras extranjero
            # letras que identifican extranjero
            numeros = "1234567890"
            dni = dni.upper()  # pasa letras a mayúsculas
            if len(dni) == 9:  # el dni debe tener 9 caracteres
                dig_control = dni[8]  # la letra
                dni = dni[:8]  # el número que son los 8 primeros
                if dni[0] in dig_ext:  # comprueba que es extranjero
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                    return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
                    # devuelve true si se dan las 2 condiciones o si no false
                else:
                    return tabla[int(dni) % 23] == dig_control
            return False

        except:
            print("Error en la aplicación")
            return None

    def visualizarCliente(self, widget):  # Metodo que se lanza al clicar en una tupla de la tabla clientes
        hola = 0
        # self.a = self.treeclientes.get_selection()
        # (tm, ti) = self.a.get_selected()
        # self.entdni.set_text(tm.get_value(ti, 0))
        # self.entmatricula.set_text(tm.get_value(ti, 1))
        # self.entapellidos.set_text(tm.get_value(ti, 2))
        # self.entnombre.set_text(tm.get_value(ti, 3))
        # self.entemail.set_text(tm.get_value(ti, 4))
        # self.entmovil.set_text(tm.get_value(ti, 5))
        # self.entfecha.set_text(tm.get_value(ti, 6))

    def visualizarComandas(self, widget):  # Metodo que se lanza al clicar en una tupla de la tabla facturas
        self.listLineasFactura.clear()
        a = self.treeFacturas.get_selection()
        (tm, ti) = a.get_selected()
        if (ti is not None):
            self.curRestaurante.execute("select * from LineasFactura where idFactura = \'" + str(tm.get_value(ti, 0)) + "\'")
            lineasFactura = self.curRestaurante.fetchall()

            for i in lineasFactura:
                self.curRestaurante.execute("select nombre, precio from servicios where idServicio = \'" + str(i[2]) + "\'")
                nombrePrecio = self.curRestaurante.fetchall()
                self.listLineasFactura.append((i[0], i[3], nombrePrecio[0][0], "%.2f" % (nombrePrecio[0][1]*i[3]) + "€"))

            self.etIdFactura.set_text(str(tm.get_value(ti, 0)))
            self.etDni2.set_text(str(tm.get_value(ti, 1)))
            self.etFecha.set_text(str(tm.get_value(ti, 4)))
            # self.entnombre.set_text(tm.get_value(ti, 3))

    def visualizarServicio(self, widget):  # Metodo que se lanza al clicar en una tupla de la tabla servicios
        hola = 0
        # self.a = self.treeclientes.get_selection()
        # (tm, ti) = self.a.get_selected()
        # self.entdni.set_text(tm.get_value(ti, 0))
        # self.entmatricula.set_text(tm.get_value(ti, 1))
        # self.entapellidos.set_text(tm.get_value(ti, 2))
        # self.entnombre.set_text(tm.get_value(ti, 3))
        # self.entemail.set_text(tm.get_value(ti, 4))
        # self.entmovil.set_text(tm.get_value(ti, 5))
        # self.entfecha.set_text(tm.get_value(ti, 6))

    def salir(self, widget, data=None):
        Gtk.main_quit()


if __name__ == "__main__":
    main = Hola()
    Gtk.main()

# if __name__ == '__main__':
# print("LA vida es dura")
# sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
# sys.exit(
# load_entry_point('pip==10.0.1', 'console_scripts', 'pip3.6')())
