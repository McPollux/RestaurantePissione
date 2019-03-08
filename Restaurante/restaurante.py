import os
import zipfile

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#from Restaurante.declaraciones import piss import --- Redundante ya que ya es importando en Restaurante.cargas
from Restaurante.cargas import *
from Restaurante.gestion_facturas import *
from Restaurante.gestion_clientes import altaCliente, modifCliente, bajaCliente, visualizarCliente
from Restaurante.gestion_servicios import altaServicio, bajaServicio

class Hola:

    def __init__(self):
        b = piss.b
        #b.add_from_file('Restaurante.glade')
        dic = {'on_PriWin_destroy': self.salir,
               'on_notebook_switch_page': self.verificarCambio,
               'on_btnMesa1_clicked': abrirFactura,
               'on_btnMesa2_clicked': abrirFactura,
               'on_btnMesa3_clicked': abrirFactura,
               'on_btnMesa4_clicked': abrirFactura,
               'on_btnMesa5_clicked': abrirFactura,
               'on_btnMesa6_clicked': abrirFactura,
               'on_btnMesa7_clicked': abrirFactura,
               'on_btnMesa8_clicked': abrirFactura,
               'on_etDni_focus_out_event': buscarCliente,
               'on_cmbProvincia_changed': cargarMunicipios,
               'on_cmbProvinciaAdm_changed': cargarMunicipios2,
               'on_btnAnhadir_clicked': anhadirComanda,
               'on_btnEliminarComanda_clicked': eliminarComanda,
               'on_btnImprimir_clicked': imprimir,
               'on_nbAdministracion_switch_page': self.verificarCambioAdministracion,
               'on_btnAltaCliente_clicked': altaCliente,
               'on_btnModifCliente_clicked': modifCliente,
               'on_btnBajaCliente_clicked': bajaCliente,
               'on_btnPrint_clicked': printPDF,
               'on_btnBajaFac_clicked': bajaFactura,
               'on_btnAltaServicio_clicked': altaServicio,
               'on_btnBajaServicio_clicked': bajaServicio,
               'on_treeSelClientes_changed': visualizarCliente,
               'on_treeSelFacturas_changed': visualizarComandas,
               'on_treeNoFuncional_changed': desSelect,
               'on_treeSelServicio_changed': self.limpiarLabel,
               'on_btnEntrar_clicked': self.login,
               'on_mbLogout_activate': self.logout,
               'on_mbComprimir_activate': self.comprimir,
               'on_mbSalir_activate': self.salir,
               'on_etContrasenha_key_press_event': self.login2
               }

        b.connect_signals(dic)

        piss.gbFactura.hide()
        cargarProvincias()
        cargarServicios()
        cargarFacturas()
        cargarClientes()
        cargarCamareros()
        cargarMesas()
        piss.priWin.set_size_request(420, 200)
        piss.venprincipal.show()
        piss.notebook.hide()

    def login(self, widget):
        """
        Evento que ocurre al intentar iniciar sesión en el programa con un usuario registrado en la base de datos, en caso de no validar visualiza un label de error
        informando del problema dado.
        """
        if piss.etUsuario.get_text() != "" and piss.etContrasenha.get_text() != "":
            piss.curRestaurante.execute(
                "select * from camareros where Nombre = '" + piss.etUsuario.get_text()+"' and password = '" + piss.etContrasenha.get_text() + "'")
            lista = piss.curRestaurante.fetchall()

            if len(lista) > 0:
                piss.notebook.show()
                piss.gbLogin.hide()
                piss.priWin.set_size_request(825, 825)
                piss.camarero = piss.etUsuario.get_text()
                piss.etUsuario.set_text("")
                piss.etContrasenha.set_text("")
                piss.lblErrorLogin.set_text("")
            else:
                piss.lblErrorLogin.set_text("Nombre de usuario o contraseña incorrectos!")
        else:
            piss.lblErrorLogin.set_text("Debes introducir tanto un nombre como contraseña")

    def login2(self, widget, key):
        """
        Evento que ocurre al intentar iniciar sesión en el programa con un usuario registrado en la base de datos, en caso de no validar visualiza un label de error
        informando del problema dado.
        """
        if key.keyval == 65293:
            if piss.etUsuario.get_text() != "" and piss.etContrasenha.get_text() != "":
                piss.curRestaurante.execute(
                    "select * from camareros where Nombre = '" + piss.etUsuario.get_text()+"' and password = '" + piss.etContrasenha.get_text() + "'")
                lista = piss.curRestaurante.fetchall()

                if len(lista) > 0:
                    piss.notebook.show()
                    piss.gbLogin.hide()
                    piss.priWin.set_size_request(825, 825)
                    piss.camarero = piss.etUsuario.get_text()
                    piss.etUsuario.set_text("")
                    piss.etContrasenha.set_text("")
                    piss.lblErrorLogin.set_text("")
                else:
                    piss.lblErrorLogin.set_text("Nombre de usuario o contraseña incorrectos!")
            else:
                piss.lblErrorLogin.set_text("Debes introducir tanto un nombre como contraseña")

    def logout(self, widget):
        """
        Evento que cierra sesión. accedido desde la pestaña indicada en el menubar
        """
        piss.notebook.hide()
        piss.gbLogin.show()
        piss.priWin.set_size_request(420, 200)

    def comprimir(self, widget):
        """
        Evento que guarda una copia de la base de datos, accedido desde la pestaña indicada en el menubar.
        Este metodo se lanza automaticamente cuando se cierra el programa.
        """
        fecha = datetime.datetime.now()
        fichzip = zipfile.ZipFile(str(fecha) + "_copia.zip", "w")
        fichzip.write("restaurante", os.path.basename("restaurante"), zipfile.ZIP_DEFLATED)
        fichzip.close()

    def verificarCambio(self, widget, redundancia, paginaPosterior):
        """
        Evento que se lanza cuando el notebook principal cambia de pestaña y tiene dos usos:
            -El primero es guardar los datos de la factura de una mesa en su objeto correspondiente en caso de que el
            usuario/camarero salga de la pestaña de factura sin imprimirla.
            -El segundo es limpiar los label de error en caso de salir de la pestaña de gestión
        """
        if (piss.notebook.get_current_page() == 1 and paginaPosterior == 0) or (piss.notebook.get_current_page() == 2 and paginaPosterior == 0 and piss.lblMesa.get_text() != "NULL"):
            guardarDatos()
        elif piss.notebook.get_current_page() == 2:
            piss.lblErrorServ.set_text("")
            piss.lblErrorClientes.set_text("")

    def verificarCambioAdministracion(self, widget, redundancia, paginaPosterior):
        """
        Evento que se lanza cuando el notebook de gestion cambia de pestaña, su eso es limpiar los label de error correspondientes
        """
        if piss.nbAdministracion.get_current_page() == 2:
            piss.lblErrorServ.set_text("")
        elif piss.nbAdministracion.get_current_page() == 0:
            piss.lblErrorClientes.set_text("")

    def limpiarLabel(self, widget):
        """
        Evento que se lanza cuando se selecciona la tupla de un servicio en la pestaña de factura, su proposito es limpiar el label de error.
        """
        piss.lblErrorServ.set_text("")

    def salir(self, widget):
        self.comprimir(widget)
        Gtk.main_quit()


if __name__ == "__main__":
    main = Hola()
    Gtk.main()
