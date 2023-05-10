from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from interfaz import contexto


Form, Window = uic.loadUiType("dialog_2.ui")


app = QApplication([])
window = Window()
form = Form()

form.setupUi(window)
contexto_1=contexto(form)
window.show()
app.exec()
