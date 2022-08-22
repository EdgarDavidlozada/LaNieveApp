
from fileinput import filename
from re import I
from LaNieve_ui import*
from functools import cache, reduce
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import numpy as np
from conexionBD import*
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,*args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.btn_enviar.clicked.connect(self.guardar_costos)
        self.btn_calcular.clicked.connect(self.guardar_fletes)
        self.btn_costos.clicked.connect(self.editar_costos)
        self.btn_fletes.clicked.connect(self.editar_fletes)
        self.btn_costos_2.clicked.connect(self.editar_costos)
        self.btn_guardarInforme.clicked.connect(self.ingresar_baseDeDatos)
        self.costos = []
        self.valores = []
        self.costomin = None
        self.tabWidget.setCurrentIndex(0)
        self.llenar_tabla()
        
    def ingresar_baseDeDatos(self):
        try:
            ingresar_solucion(int(self.nviajes_villavicencio.text()), int(self.nviajes_casanare.text()),int(self.nviajes_yopal.text()),int(self.nviajes_bogota.text()),int(self.costomin),int(self.valores[0]),int(self.valores[1]))
            fecha_hora = datetime.now()
            titulo = f'INFORME_COSTO_MINIMO_{fecha_hora}'
            id_solucion = buscar_ultimaSolucion()
            ingresar_informe(titulo,fecha_hora,self.lbl_analisis.toPlainText(),int(id_solucion[0]))
            id_informe = buscar_ultimoInforme()
            for i in range(4):
                ingresar_costo(int(id_informe[0]),i+1,int(self.costos[i]))
                ingresar_distribucion(int(id_informe[0]),i+1,int(self.Tabla_tiendas.item(0,i).text()),int(self.Tabla_mayoristas.item(0,i).text()))
            ingresar_flete_min_mes(int(id_informe[0]),int(self.ctiendas_fletes.text()),int(self.cmayoristas_fletes.text()))
            QMessageBox.about(self, "Mensaje", "Informe guardado en la base de datos")
            self.tab_informes.setEnabled(True)
            self.tab_minimizacion.setEnabled(False)
            self.tabWidget.setCurrentIndex(3)
            self.llenar_tabla()
            
        except ValueError:
            QMessageBox.about(self, "Error", "Hubo un error al intentar guardar el informe")
            
    def guardar_costos(self):
        vc_vill = int(self.ValCostoVillavicencio.text())
        vc_cas = int(self.ValCostoCasanare.text())
        vc_yop = int(self.ValCostoYopal.text())
        vc_bog = int(self.ValCostoBogota.text())
        self.tab_fletes.setEnabled(True)
        self.tab_costos.setEnabled(False)
        self.tabWidget.setCurrentIndex(1)
        self.costos = costos(vc_vill,vc_cas,vc_yop,vc_bog)
        
      
    def guardar_fletes(self):
        ctiendas_fletes = -int(self.ctiendas_fletes.text())
        ctiendas_villavicencio = -int(self.Tabla_tiendas.item(0, 0).text())
        ctiendas_casanare = -int(self.Tabla_tiendas.item(0, 1).text())
        ctiendas_yopal = -int(self.Tabla_tiendas.item(0, 2).text())
        ctiendas_bogota = -int(self.Tabla_tiendas.item(0, 3).text())
        cmayoristas_fletes = -int(self.cmayoristas_fletes.text())
        cmayoristas_villavicencio = -int(self.Tabla_mayoristas.item(0, 0).text())
        cmayoristas_casanare = -int(self.Tabla_mayoristas.item(0, 1).text())
        cmayoristas_yopal = -int(self.Tabla_mayoristas.item(0, 2).text())
        cmayoristas_bogota = -int(self.Tabla_mayoristas.item(0, 3).text())
        self.tab_fletes.setEnabled(False)
        self.tab_minimizacion.setEnabled(True)
        self.tabWidget.setCurrentIndex(2)
        funcionObjetivo=self.costos
        restriccion1=fletes_tiendas(ctiendas_villavicencio,ctiendas_casanare,ctiendas_yopal,ctiendas_bogota,ctiendas_fletes)
        restriccion2=fletes_mayoristas(cmayoristas_villavicencio,cmayoristas_casanare,cmayoristas_yopal,cmayoristas_bogota,cmayoristas_fletes)
        metodo_simplex(self,funcionObjetivo,restriccion1,restriccion2)
      
    def editar_costos(self):
        self.tab_costos.setEnabled(True)
        self.tab_fletes.setEnabled(False)
        self.tab_minimizacion.setEnabled(False)
        self.tabWidget.setCurrentIndex(0)
    
    def editar_fletes(self):
        self.tab_fletes.setEnabled(True)
        self.tab_minimizacion.setEnabled(False)
        self.tabWidget.setCurrentIndex(1)
         
    def llenar_tabla(self):
        self.tablaInformes.clearContents()
        nombreColumnas = ("ID INFORME","TITULO", "FECHA", "ANALISIS", "ID SOLUCION")
        informes = buscar_all_informes()
        
        # Deshabilitar edición
        self.tablaInformes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tablaInformes.setDragDropOverwriteMode(False)
        # Seleccionar toda la fila
        self.tablaInformes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tablaInformes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # Especifica dónde deben aparecer los puntos suspensivos "..." cuando se muestran
        # textos que no encajan
        self.tablaInformes.setTextElideMode(QtCore.Qt.ElideRight)# Qt.ElideNone
        # Establecer el ajuste de palabras del texto 
        self.tablaInformes.setWordWrap(False)
        # Deshabilitar clasificación
        self.tablaInformes.setSortingEnabled(False)
        # Establecer el número de columnas
        self.tablaInformes.setColumnCount(6)
        # Establecer el número de filas
        self.tablaInformes.setRowCount(0)
        # Alineación del texto del encabezado
        self.tablaInformes.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|
                                                          QtCore.Qt.AlignCenter)
        # Deshabilitar resaltado del texto del encabezado al seleccionar una fila
        self.tablaInformes.horizontalHeader().setHighlightSections(False)
        # Hacer que la última sección visible del encabezado ocupa todo el espacio disponible
        self.tablaInformes.horizontalHeader().setStretchLastSection(True)
        # Ocultar encabezado vertical
        self.tablaInformes.verticalHeader().setVisible(False)
        # Dibujar el fondo usando colores alternados
        self.tablaInformes.setAlternatingRowColors(True)
        # Establecer altura de las filas
        self.tablaInformes.verticalHeader().setDefaultSectionSize(20)
        
        row = 0
        print(informes)
        # Establecer el número de columnas
        self.tablaInformes.setColumnCount(5)
        # Establecer el número de filas
        self.tablaInformes.setRowCount(0)
        self.tablaInformes.setHorizontalHeaderLabels(nombreColumnas)
        for endian in informes:
            self.tablaInformes.setRowCount(row + 1)
            self.tablaInformes.setItem(row, 0,  QtWidgets.QTableWidgetItem(endian[0]))
            self.tablaInformes.setItem(row, 1, QtWidgets.QTableWidgetItem(endian[1]))
            self.tablaInformes.setItem(row, 2, QtWidgets.QTableWidgetItem(endian[2]))
            self.tablaInformes.setItem(row, 3, QtWidgets.QTableWidgetItem(endian[3]))
            self.tablaInformes.setItem(row, 4, QtWidgets.QTableWidgetItem(endian[4]))
            row += 1
    
def costos(cosVillavicencio,cosCasanare,cosYopal,cosBogota):
    costos = [cosVillavicencio, cosCasanare,cosYopal,cosBogota]
    return costos

def fletes_tiendas(cantVillavicencio,cantCasanare,cantYopal,cantBogota,cantTotal):
    fletes_tiendas = [cantVillavicencio,cantCasanare,cantYopal,cantBogota,cantTotal]
    return fletes_tiendas

def fletes_mayoristas(cantVillavicencio,cantCasanare,cantYopal,cantBogota,cantTotal):
    fletes_mayoristas = [cantVillavicencio,cantCasanare,cantYopal,cantBogota,cantTotal]
    return fletes_mayoristas    

def metodo_simplex(self,funcionObjetivo,restriccion1,restriccion2):
    
    C = funcionObjetivo
    desigualdades = [restriccion1[-1],restriccion2[-1]]
    restriccion1.pop()
    restriccion2.pop()
    A = [restriccion1,restriccion2]
    b = [desigualdades]
    X0_bounds = [1,None]
    res = linprog(C,A,b,bounds=(X0_bounds))
    #print(res)
    #print("Valor optimo: ",res.fun,"\nX:",res.x)
    mostrar_solucion(self,res.x)
    grafica_pastel(self,res.x,restriccion1,restriccion2)

def mostrar_solucion(self,cantViajes):
    nviajes_villavicencio = round(cantViajes[0])
    nviajes_casanare = round(cantViajes[1])
    nviajes_yopal = round(cantViajes[2])
    nviajes_bogota = round(cantViajes[3])
    viajes = [nviajes_villavicencio,nviajes_casanare,nviajes_yopal,nviajes_bogota]
    self.costomin = reduce(lambda a, b: a + b,list(map(lambda x,y: x*y ,viajes,self.costos)))
    costo_minimo = (f'{self.costomin:,.2f}')
    self.nviajes_villavicencio.setText(str(nviajes_villavicencio))
    self.nviajes_casanare.setText(str(nviajes_casanare))
    self.nviajes_yopal.setText(str(nviajes_yopal))
    self.nviajes_bogota.setText(str(nviajes_bogota))
    self.lbl_min.setText(str(costo_minimo))
    self.imagen_pastel.setPixmap(QtGui.QPixmap(""))
    plt.close()
    

def grafica_pastel(self,cantViajes,tiendas,mayoristas):
    ptiendas = list(map(lambda x: x*-1,tiendas))
    #print(ptiendas)
    pmayoristas = list(map(lambda x: x*-1,mayoristas))
    #print(pmayoristas)
    viajesTiendas = reduce(lambda a,b:a+b, list(map(lambda x,y: round(x)*y,cantViajes,ptiendas)))
    viajesMayoristas = reduce(lambda a,b:a+b, list(map(lambda x,y: round(x)*y,cantViajes,pmayoristas)))
    self.valores = np.array([viajesTiendas,viajesMayoristas])
    etiquetas =["Tiendas","Mayoristas"]
    #print(valores)plt.close()
    #print(etiquetas)
    plt.style.use('ggplot')
    plt.pie(self.valores,labels=etiquetas,startangle=90,autopct="%0.1f %%",shadow=True)
    plt.axis('equal')
    legend1 = f'Tiendas visitadas: {self.valores[0]}'
    legend2 = f'Mayoristas visitados: {self.valores[1]}'
    plt.legend([legend1,legend2])
    plt.title("Porcentaje total de viajes por tiendas y mayoristas")
    plt.savefig('Grafica_pastel.jpg'    ,bbox_inches='tight')
    image = QtGui.QImage('Grafica_pastel.jpg')
    pixi = QtGui.QPixmap.fromImage(image).scaled(241, 171, QtCore.Qt.KeepAspectRatio)
    self.imagen_pastel.setPixmap(pixi)
    self.imagen_pastel.setAlignment(QtCore.Qt.AlignCenter)
    plt.show()

if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()