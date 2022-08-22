from conexionBD import*

def llenar_tabla():
    
    rt = buscar_all_informes()
    
    print(rt)
    
llenar_tabla()