from PyQt5.QtWidgets import QFileDialog 
import random
from time import sleep
from hiloEntrenamiento import contexEntrenamiento
import pyqtgraph as pt


def funcion_lineal(x):
    return x

def funcion_escalonada(x):
    if x>=0:
        return 1.0
    else:
        return 0.0




class contexto():

    datos_entras = []
    datos_salidas = []
    contador_2 = 0
    contador_3 = 0
    contador = 0
    error_maximo =0
    iteraciones=0
    rata=0
    tipo=0
    pesos=[]
    umbrales=[]
    datos_x=[]
    datos_y=[]

    def __init__(self, form) -> None:
        self.form = form
        self.funcion_activacion=funcion_escalonada
        
        form.button_cargar.clicked.connect(self.cargar_archivo)
        form.bt_exportar.clicked.connect(self.exportar_confi)
        form.bt_importar_2.clicked.connect(self.importar_confi)
        form.bt_importar.clicked.connect(self.importar_data)
        form.bt_entrenar.clicked.connect(self.setVieEntrenar)
        form.bt_simular.clicked.connect(self.setVieSimular)
        form.bt_cargar.clicked.connect(self.setVieCargar)
        form.bt_c_3.clicked.connect(self.cacelarentranimiento)
        form.caja_error.textChanged.connect(self.mapeo2)
        form.caja_iteraciones.textChanged.connect(self.mapeo_3)
        form.caja_rata.textChanged.connect(self.mapeo_4)
        form.combo_accion.currentIndexChanged.connect(self.combo)
        form.bt_entrenar_2.clicked.connect(self.entrenamiento)
        
        self.grafica=pt.PlotWidget(title ="GRAFICA ENTRENAMIENTO")
        self.grafica.setBackground('w')
        pen = pt.mkPen(color=(255, 0, 0))
        self.line=self.grafica.plot(self.datos_x,self.datos_y,pen)
        form.grafica.addWidget(self.grafica)

        self.grafica_2=pt.PlotWidget(title ="GRAFICA SIMULAR")
        self.grafica_2.setBackground('w')
        pen = pt.mkPen(color=(255, 0, 0))
        self.line=self.grafica_2.plot(self.datos_x,self.datos_y,pen)
        form.grafica_2.addWidget(self.grafica_2)

        
       

    def cargar_archivo(self):
        dialo = QFileDialog()
        dialo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialo.setNameFilter("datos en txt(*.txt)")
        if dialo.exec_():
            nombre_archivo = dialo.selectedFiles()
            self.cargar_datos(nombre_archivo[0])
        self.mapeo()
        self.generar_pesos()

    def cargar_datos(self, ubicacion):

        with open(ubicacion, 'r') as f:
            documento = f.read()
            documento = documento.split('\n')
            for set in documento:
                linea = set.split('=')
                cas_linea = linea[1].split(' ')
                if linea[0] == 'E':
                    self.datos_entras.append(list(map(float,cas_linea)))
                    self.contador += 1
                    self.contador_2 = cas_linea.__len__()
                else:
                    self.datos_salidas.append(list(map(float,cas_linea)))
                    self.contador_3 += 1
            ##print(self.datos_entras, self.datos_salidas)
            ##print(self.contador, self.contador_2, self.contador_3)

    def mapeo(self):
        self.form.caja_entrada.setText(str(self.contador))
        self.form.caja_salida.setText(str(self.contador_3))
        self.form.caja_patron.setText(str(self.contador_2))
    
    
    def mapeo2(self,text):
        try:
            self.error_maximo=float(text)
            #print(self.error_maximo)
        except ValueError:
            self.form.caja_error.setText(str(self.error_maximo))
    
    def mapeo_3(self,text):
        try:
            self.iteraciones=float(text)
            #print(self.iteraciones)
        except ValueError:
            self.form.caja_iteraciones.setText(str(self.iteraciones))
    
    def mapeo_4(self,text):
        try:
            self.rata=float(text)
            #print(self.rata)
        except ValueError:
            self.form.caja_rata.setText(str(self.rata))
    
    def combo(self,numero):
        self.tipo=numero
        if numero ==0 : 
            self.funcion_activacion=funcion_escalonada
        if numero==1:
            self.funcion_activacion=funcion_lineal
        #print(self.tipo)

    
    def generar_pesos(self):
        for entrada in range(0,self.contador):
            fila_actual=[]
            for salida in range(0,self.contador_3):
                fila_actual.append(random.uniform(-1,1))
                if entrada==0 & salida==0:
                 self.umbrales.append(random.uniform(-1,1))
            self.pesos.append(fila_actual)
        #print(self.pesos)
        #print(self.umbrales)

    def setVieCargar(self):
         self.form.stackedWidget.setCurrentWidget(self.form.page_cargar)


    def setVieEntrenar(self):
        self.form.stackedWidget.setCurrentWidget(self.form.page_entrenar)

        pass
    
    def setVieSimular(self):
        self.form.stackedWidget.setCurrentWidget(self.form.page_simular)
    

    def entrenamiento(self):
        self.thead_entrenamiento = contexEntrenamiento(self)
        self.thead_entrenamiento.update.connect(self.updateUi)
        self.thead_entrenamiento.start()

    def cacelarentranimiento(self):
        self.thead_entrenamiento.terminate()
    
    def updateUi(self):
        self.datos_x.append(self.thead_entrenamiento.contador_iteracion)
        self.datos_y.append(self.thead_entrenamiento.error_maximo)
        self.line.setData(self.datos_x,self.datos_y)
        self.form.line_iteracion_3.setText(str(self.thead_entrenamiento.contador_iteracion))
        self.form.line_error_3.setText(str(self.thead_entrenamiento.error_maximo))

    
    def exportar_confi(self):
        dialo = QFileDialog()
        dialo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialo.setNameFilter("datos en txt(*.txt)")
        if dialo.exec_():
            nombre_archivo = dialo.selectedFiles()
            self.exportar_confi(nombre_archivo[0]) 
    
    def importar_confi(self):
        dialo = QFileDialog()
        dialo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialo.setNameFilter("datos en txt(*.txt)")
        if dialo.exec_():
            nombre_archivo = dialo.selectedFiles()
            self.importar_confi(nombre_archivo[0])

    def importar_data(self):
        dialo = QFileDialog()
        dialo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialo.setNameFilter("datos en txt(*.txt)")
        if dialo.exec_():
            nombre_archivo = dialo.selectedFiles()
            self.importar_data(nombre_archivo[0])


