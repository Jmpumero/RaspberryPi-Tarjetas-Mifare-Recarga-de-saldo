# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_ayuda.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(222, 224)
        Dialog.setMinimumSize(QtCore.QSize(222, 224))
        Dialog.setMaximumSize(QtCore.QSize(222, 224))
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 10, 311, 341))
        self.frame.setMinimumSize(QtCore.QSize(311, 341))
        self.frame.setMaximumSize(QtCore.QSize(311, 341))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.nombre_label = QtWidgets.QLabel(self.frame)
        self.nombre_label.setGeometry(QtCore.QRect(20, 50, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nombre_label.setFont(font)
        self.nombre_label.setObjectName("nombre_label")
        self.correo_label = QtWidgets.QLabel(self.frame)
        self.correo_label.setGeometry(QtCore.QRect(10, 80, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.correo_label.setFont(font)
        self.correo_label.setObjectName("correo_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.nombre_label.setText(_translate("Dialog", "Autor: José J Medina P"))
        self.correo_label.setText(_translate("Dialog", "Correo:  jmpumero@gmail.com"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
