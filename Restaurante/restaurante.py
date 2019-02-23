gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#from Restaurante.declaraciones import piss import --- Redundante ya que ya es importando en Restaurante.cargas
from Restaurante.cargas import *
from Restaurante.gestion_facturas import abrirFactura, buscarCliente, anhadirComanda, eliminarComanda, imprimir, printPDF, bajaFactura, visualizarComandas, guardarDatos
from Restaurante.gestion_clientes import altaCliente, modifCliente, bajaCliente, visualizarCliente
from Restaurante.gestion_servicios import altaServicio, bajaServicio

class Hola:

    def __init__(self):
        b = Gtk.Builder()
        b.add_from_file('Restaurante.glade')
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
               'on_treeNoFuncional_changed': self.select,
               'on_treeSelServicio_changed': self.treeSelServicio,
               'on_mbSalir_activate': self.salir,
               }

        b.connect_signals(dic)

        piss.gbFactura.hide()
        cargarProvincias()
        cargarServicios()
        cargarFacturas()
        cargarClientes()
        cargarCamareros()
        cargarMesas()
        piss.venprincipal.show()

    def verificarCambio(self, widget, redundancia, paginaPosterior):
        if (piss.notebook.get_current_page() == 1 and paginaPosterior == 0) or (piss.notebook.get_current_page() == 2 and paginaPosterior == 0 and piss.lblMesa.get_text()!= "NULL"):
            guardarDatos()
        elif piss.notebook.get_current_page() == 2:
            piss.lblErrorServ.set_text("")
            piss.lblErrorClientes.set_text("")

    def verificarCambioAdministracion(self, widget, redundancia, paginaPosterior):
        if piss.nbAdministracion.get_current_page() == 2:
            piss.lblErrorServ.set_text("")
        elif piss.nbAdministracion.get_current_page() == 0:
            piss.lblErrorClientes.set_text("")

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

    def treeSelServicio(self, widget):
        piss.lblErrorServ.set_text("")

    def salir(self, widget, data=None):
        Gtk.main_quit()


if __name__ == "__main__":
    main = Hola()
    Gtk.main()
