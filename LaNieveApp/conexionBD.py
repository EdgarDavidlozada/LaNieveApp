import sqlite3

def ingresar_solucion(x1,x2,x3,x4,costoMinimo,ViaTiendas,ViaMayoristas):
    conexion=sqlite3.connect("LaNieveBD")
    conexion.execute("insert into soluciones(villavicencio,casanare,yopal,bogota,costo_min,viajes_tiendas,viajes_mayoristas) values (?,?,?,?,?,?,?)", (x1,x2,x3,x4,costoMinimo,ViaTiendas,ViaMayoristas))
    conexion.commit()
    conexion.close()

def ingresar_informe(titulo,fecha,analisis,id_solucion):
    conexion=sqlite3.connect("LaNieveBD")
    conexion.execute("insert into informes(titulo,fecha,analisis,id_solucion) values (?,?,?,?)", (titulo,fecha,analisis,id_solucion))
    conexion.commit()
    conexion.close()

def ingresar_costo(id_informe,id_destino,costo):
    conexion=sqlite3.connect("LaNieveBD")
    conexion.execute("insert into costos(id_informe,id_destino,costo) values (?,?,?)", (id_informe,id_destino,costo))
    conexion.commit()
    conexion.close()

def ingresar_distribucion(id_informe,id_destino,tiendas,mayoristas):
    conexion=sqlite3.connect("LaNieveBD")
    conexion.execute("insert into distribuciones(id_informe,id_destino,tiendas,mayoristas) values (?,?,?,?)", (id_informe,id_destino,tiendas,mayoristas))
    conexion.commit()
    conexion.close()
    
def ingresar_flete_min_mes(id_informe,tiendas,mayoristas):
    conexion=sqlite3.connect("LaNieveBD")
    conexion.execute("insert into fletes_minimos_mes(id_informe,tiendas,mayoristas) values (?,?,?)", (id_informe,tiendas,mayoristas))
    conexion.commit()
    conexion.close()
    
def buscar_ultimaSolucion():
    conexion=sqlite3.connect("LaNieveBD")
    cur = conexion.cursor()
    cur.execute("select id_solucion from soluciones order by id_solucion desc limit 1")
    rt = cur.fetchone()
    conexion.commit()
    conexion.close()
    return rt

def buscar_ultimoInforme():
    conexion=sqlite3.connect("LaNieveBD")
    cur = conexion.cursor()
    cur.execute("select id_informe from informes order by id_informe desc limit 1")
    rt = cur.fetchone()
    conexion.commit()
    conexion.close()
    return rt


def buscar_all_informes():
    conexion=sqlite3.connect("LaNieveBD")
    cur = conexion.cursor()
    cur.execute("select * from informes order by fecha desc")
    rt = cur.fetchall()
    conexion.commit()
    conexion.close()
    return rt