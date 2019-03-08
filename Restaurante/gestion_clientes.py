from Restaurante.declaraciones import piss
from Restaurante.cargas import cargarClientes


def altaCliente(widget):
    """
     Evento que se lanza al pulsar el boton correspondiente en el gestor de clientes. En caso de introducir la información
     adecuadamente da de alta al cliente en la base de datos y limpia los campos.
    """
    if piss.etDniAdm.get_text() is "":
        piss.lblErrorClientes.set_text("El DNI no puede estar vacio!")
        return
    if not validoDNI(piss.etDniAdm.get_text()):
        piss.lblErrorClientes.set_text("El DNI no cumple el formato preestablecido")
        return

    if not validoDuplicidad(piss.etDniAdm.get_text()):
        piss.lblError.set_text("Este cliente ya existe en la base de datos!")
        return

    tree_prov = piss.cmbProvinciaAdm.get_active_iter()
    tree_local = piss.cmbCiudadAdm.get_active_iter()
    model = piss.cmbProvinciaAdm.get_model()
    prov = model[tree_prov][0]
    model = piss.cmbCiudadAdm.get_model()
    localidad = model[tree_local][0]

    lista = (
        piss.etDniAdm.get_text(), piss.etNombreAdm.get_text(), piss.etApellidosAdm.get_text(),
        piss.etDireccionAdm.get_text(),
        prov,
        localidad)
    piss.curRestaurante.execute("insert into clientes values (?, ?, ?, ?, ?, ?)", lista)
    piss.conexPissione.commit()
    piss.lblErrorClientes.set_text("")
    cargarClientes()

def validoDuplicidad(dni):
    """
     Metodo usado en altaCliente parqa confirmar que el DNI introducido no se encuentra ya en la base de datos.
    """
    piss.curRestaurante.execute("select dni from clientes")
    resultado = piss.curRestaurante.fetchall()
    for i in range(len(resultado)):
        if dni == resultado[i][0]:
            return False
    return True


def validoDNI(dni):
    """
     Metodo usado en altaCliente parqa confirmar que el DNI introducido tiene un formato adecuado.
    """
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


def modifCliente(widget):
    """
     Evento que se lanza al pulsar el boton correspondiente en el gestor de clientes. En caso de introducir la información
     adecuadamente modifica la información(a excepción del propio DNI) del cliente en la base de datos y limpia los campos.
    """
    piss.curRestaurante.execute("select count(dni) from clientes where dni = '" + piss.etDniAdm.get_text() + "'")
    resultado = piss.curRestaurante.fetchall()
    if piss.etDniAdm.get_text() == "0":
        piss.lblErrorClientes.set_text("No puedes modificar al cliente anónimo")
    else:
        if resultado[0][0] is not 0:
            tree_prov = piss.cmbProvinciaAdm.get_active_iter()
            tree_local = piss.cmbCiudadAdm.get_active_iter()
            model = piss.cmbProvinciaAdm.get_model()
            prov = model[tree_prov][0]
            model = piss.cmbCiudadAdm.get_model()
            localidad = model[tree_local][0]

            lista = (piss.etNombreAdm.get_text(), piss.etApellidosAdm.get_text(), piss.etDireccionAdm.get_text(),
                     prov,
                     localidad,
                     piss.etDniAdm.get_text())

            piss.curRestaurante.execute("update clientes set nombre = ?, apellidos = ?, direccion = ?, provincia = ?, ciudad = ? where dni = ?", lista)
            piss.conexPissione.commit()
            cargarClientes()
            piss.lblErrorClientes.set_text("")
        else:
            piss.lblErrorClientes.set_text("El DNI introducido no se encuentra en la base de datos!")

def bajaCliente(widget):
    """
    Evento que se lanza cuando el usuario pulsa el botón correspondiente para borrar al cliente de la base de datos a
    peticion del propio cliente.
    """
    a = piss.treeClientes.get_selection()
    (tm, ti) = a.get_selected()
    if tm.get_value(ti,0) == "0":
        piss.lblErrorClientes.set_text("No puedes eliminar al cliente anónimo")
    else:
        piss.curRestaurante.execute("delete from clientes where dni='" + tm.get_value(ti, 0) + "'")
        piss.conexPissione.commit()
        cargarClientes()

        piss.lblErrorClientes.set_text("")


def visualizarCliente(widget):  # Metodo que se lanza al clicar en una tupla de la tabla clientes
    """
    Evento que se lanza cuando el usuario pulsa en una tupla de la tabla cliente y su tarea es introducir automaticamente
    la información del cliente en los entry/combobox.
    """
    vaciarAdministracionClientes()
    a = piss.treeClientes.get_selection()
    (tm, ti) = a.get_selected()
    if ti is not None:
        piss.etDniAdm.set_text(tm.get_value(ti, 0))
        piss.etNombreAdm.set_text(tm.get_value(ti, 1))
        piss.etApellidosAdm.set_text(tm.get_value(ti, 2))
        piss.etDireccionAdm.set_text(tm.get_value(ti, 3))
        piss.cmbProvinciaAdm.set_active(idProvincia(tm.get_value(ti, 4)))
        piss.cmbCiudadAdm.set_active(idCiudad2(str(tm.get_value(ti, 5))))


def idProvincia(nombre):
    """
    Metodo que dado un nombre de provincia devuelve su id en la base de datos.
    """
    piss.curReverb.execute("select id, provincia from provincias")
    provincias = piss.curReverb.fetchall()
    for i in provincias:
        if i[1] == nombre:
            return int(i[0] - 1)


def idCiudad2(nombre):
    """
    Metodo que dado un nombre de ciudad devuelve su id en su lista.
    """
    cont = 0
    for i in piss.listMunicipios2:
        if i[0] == nombre:
            return cont
        cont += 1


def vaciarAdministracionClientes():
    """
    Limpia todos los campos.
    """
    piss.etDniAdm.set_text("")
    piss.etDireccionAdm.set_text("")
    piss.etNombreAdm.set_text("")
    piss.etApellidosAdm.set_text("")
    piss.cmbProvinciaAdm.set_active(-1)
    piss.cmbCiudadAdm.set_active(-1)
    piss.lblErrorClientes.set_text("")

#EOF