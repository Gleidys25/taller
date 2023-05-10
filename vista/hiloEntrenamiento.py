import typing
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import sleep


class contexEntrenamiento(QThread):

    update = pyqtSignal()
    contador_iteracion = 0
    error_maximo = 999999999999999.0

    def __init__(self, parent) -> None:
        QThread.__init__(self)
        self._parent = parent

    def run(self):

        while (self.contador_iteracion < self._parent.iteraciones) & (self.error_maximo > self._parent.error_maximo):
            # print(self.contador_iteracion)
            # print(self._parent.contador)

             
            error_patrones = []
            for ubicacion_patron in range(0,self._parent.contador_2):
                patron=[self._parent.datos_entras[i][ubicacion_patron] for i in range(0,self._parent.contador)]
                # print(patron)
                salida = self.regla_delta(self._parent.contador_3, self._parent.contador, self._parent.pesos,
                                         self._parent.umbrales, patron,self._parent.funcion_activacion)
                
                # print(salida)
                error = self.calcularerror_relativo(
                    salida, self._parent.datos_salidas, ubicacion_patron)
               
                error_patrones.append(abs( sum(error))/salida.__len__())
                print(error)
                print("=======================")
                nuevos_pesos = []
                nuevos_umbrales=[]
                for j in range(0,self._parent.pesos.__len__()):
                    nueva_pila_pesos = []
                    for i in range(0,self._parent.pesos[j].__len__()):
                        nueva_pila_pesos.append(self._parent.pesos[j][i]+self._parent.rata
                                                        * error[i]*patron[j])
                    nuevos_pesos.append(nueva_pila_pesos)
                    # print(nueva_pila_pesos)
                for j in range(0, self._parent.umbrales.__len__()):
                    nuevo_umbral= self._parent.umbrales[j]+ self._parent.rata * error[j]*1
                    nuevos_umbrales.append(nuevo_umbral)
                self._parent.pesos=nuevos_pesos  
                self._parent.umbrales=nuevos_umbrales  
                ubicacion_patron += 1
            error_iteracion = sum(error_patrones)/ \
                                  self._parent.datos_entras.__len__()
            self.error_maximo = error_iteracion
            self.contador_iteracion += 1
            # print(error_patrones)
            
            self.update.emit()
            sleep(3)



    def regla_delta(self, numerosalida, numero_entrada, pesos, umbrales, patron,funcion_activacion):
        salida = []
        for i in range(0, numerosalida):
            sumatoria = 0
            for j in range(0, numero_entrada):
                # #print(patron[j])
                # #print( pesos[j][i])
                sumatoria += patron[j] * pesos[j][i]
            salida.append(funcion_activacion(sumatoria-umbrales[i]))

        return salida


    def calcularerror_relativo(self, salida, salida_esperadas,numero_patrones):  
        _salida_esperdas = []

        for i in range(0, salida.__len__()):
            _salida_esperdas.append(salida_esperadas[i][numero_patrones])
        return list(map(lambda x, y: y-x,salida,_salida_esperdas))    
