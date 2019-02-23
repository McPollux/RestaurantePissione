from Restaurante.declaraciones import piss
from Restaurante.cargas import cargarClientes

def altaCliente(data, widget):
    if piss.etDniAdm.get_text() is not "":
        tree_prov = piss.cmbProvinciaAdm.get_active_iter()
        tree_local = piss.cmbCiudadAdm.get_active_iter()
        model = piss.cmbProvinciaAdm.get_model()
        prov = model[tree_prov][0]
        model = piss.cmbCiudadAdm.get_model()
        localidad = model[tree_local][0]

        lista = (
            piss.etDniAdm.get_text(), piss.etNombreAdm.get_text(), piss.etApellidosAdm.get_text(), piss.etDireccionAdm.get_text(),
            prov,
            localidad)
        piss.curRestaurante.execute("insert into clientes values (?, ?, ?, ?, ?, ?)", lista)
        piss.conexPissione.commit()
        piss.lblErrorClientes.set_text("")
    else:
        piss.lblErrorClientes.set_text("El DNI no puede estar vacio!")
    cargarClientes()

def modifCliente(data, widget):
    piss.curRestaurante.execute("select count(dni) from clientes where dni = '" + piss.etDniAdm.get_text() + "'")
    resultado = piss.curRestaurante.fetchall()
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

def bajaCliente(data, widget):
    a = piss.treeClientes.get_selection()
    (tm, ti) = a.get_selected()
    piss.curRestaurante.execute("delete from clientes where dni='" + tm.get_value(ti, 0) + "'")
    piss.conexPissione.commit()
    cargarClientes()

    piss.lblErrorClientes.set_text("")

def visualizarCliente(data, widget):  # Metodo que se lanza al clicar en una tupla de la tabla clientes
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

def idProvincia(nombre):  #Metodo duplicado de la seccion facturas
    piss.curReverb.execute("select id, provincia from provincias")
    provincias = piss.curReverb.fetchall()
    for i in provincias:
        if i[1] == nombre:
            return int(i[0] -1)

def idCiudad2(nombre):
    cont = 0
    for i in piss.listMunicipios2:
        if i[0] == nombre:
            return cont
        cont += 1

def vaciarAdministracionClientes():
    piss.etDniAdm.set_text("")
    piss.etDireccionAdm.set_text("")
    piss.etNombreAdm.set_text("")
    piss.etApellidosAdm.set_text("")
    piss.cmbProvinciaAdm.set_active(-1)
    piss.cmbCiudadAdm.set_active(-1)

#EOF