from PyQt5.QtWidgets import QApplication, QLabel
import sys


if __name__ =='__main__':
    main=QApplication(sys.argv)
    label=QLabel('Hola World')
    label.show
    sys.exit(main.exec_())


