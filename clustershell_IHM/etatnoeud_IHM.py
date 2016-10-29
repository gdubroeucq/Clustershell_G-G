# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'etatnoeud_IHM.ui'
#
# Created: Sat Oct 29 18:55:35 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(511, 544)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 500, 95, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 500, 95, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 461, 411))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 471, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Information sur les noeuds", None))
        self.pushButton.setText(_translate("Form", "OK", None))
        self.pushButton_2.setText(_translate("Form", "Annuler", None))
        self.lineEdit.setPlaceholderText(_translate("Form", "noeuds", None))
        self.pushButton_3.setText(_translate("Form", "Parcourir", None))

