# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'features_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_SegmenationMetrics(object):
    def setupUi(self, SegmenationMetrics):
        SegmenationMetrics.setObjectName(_fromUtf8("SegmenationMetrics"))
        SegmenationMetrics.resize(402, 319)
        self.buttonBox = QtGui.QDialogButtonBox(SegmenationMetrics)
        self.buttonBox.setGeometry(QtCore.QRect(30, 270, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(SegmenationMetrics)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 40, 141, 229))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.area_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.area_check.setFont(font)
        self.area_check.setChecked(True)
        self.area_check.setObjectName(_fromUtf8("area_check"))
        self.verticalLayout_2.addWidget(self.area_check)
        self.circularity_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.circularity_check.setFont(font)
        self.circularity_check.setChecked(True)
        self.circularity_check.setObjectName(_fromUtf8("circularity_check"))
        self.verticalLayout_2.addWidget(self.circularity_check)
        self.intensity_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.intensity_check.setFont(font)
        self.intensity_check.setChecked(True)
        self.intensity_check.setObjectName(_fromUtf8("intensity_check"))
        self.verticalLayout_2.addWidget(self.intensity_check)
        self.angle_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.angle_check.setFont(font)
        self.angle_check.setChecked(True)
        self.angle_check.setObjectName(_fromUtf8("angle_check"))
        self.verticalLayout_2.addWidget(self.angle_check)
        self.directionality_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.directionality_check.setFont(font)
        self.directionality_check.setChecked(True)
        self.directionality_check.setObjectName(_fromUtf8("directionality_check"))
        self.verticalLayout_2.addWidget(self.directionality_check)
        self.solidity_check = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.solidity_check.setFont(font)
        self.solidity_check.setChecked(True)
        self.solidity_check.setObjectName(_fromUtf8("solidity_check"))
        self.verticalLayout_2.addWidget(self.solidity_check)
        self.verticalLayoutWidget = QtGui.QWidget(SegmenationMetrics)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 40, 171, 111))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.linearity_check = QtGui.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.linearity_check.setFont(font)
        self.linearity_check.setChecked(True)
        self.linearity_check.setObjectName(_fromUtf8("linearity_check"))
        self.verticalLayout.addWidget(self.linearity_check)
        self.convergence_check = QtGui.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.convergence_check.setFont(font)
        self.convergence_check.setChecked(True)
        self.convergence_check.setObjectName(_fromUtf8("convergence_check"))
        self.verticalLayout.addWidget(self.convergence_check)
        self.distribution_check = QtGui.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.distribution_check.setFont(font)
        self.distribution_check.setChecked(True)
        self.distribution_check.setObjectName(_fromUtf8("distribution_check"))
        self.verticalLayout.addWidget(self.distribution_check)
        self.label = QtGui.QLabel(SegmenationMetrics)
        self.label.setGeometry(QtCore.QRect(230, 20, 111, 21))
        self.label.setMaximumSize(QtCore.QSize(16777191, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(SegmenationMetrics)
        self.label_2.setGeometry(QtCore.QRect(50, 20, 91, 21))
        self.label_2.setMaximumSize(QtCore.QSize(16777191, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(SegmenationMetrics)
        self.label_3.setGeometry(QtCore.QRect(260, 170, 51, 21))
        self.label_3.setMaximumSize(QtCore.QSize(16777191, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayoutWidget = QtGui.QWidget(SegmenationMetrics)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 190, 160, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.scale_spin = QtGui.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.scale_spin.setObjectName(_fromUtf8("scale_spin"))
        self.horizontalLayout.addWidget(self.scale_spin)
        self.line = QtGui.QFrame(SegmenationMetrics)
        self.line.setGeometry(QtCore.QRect(200, 150, 161, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(SegmenationMetrics)
        self.line_2.setGeometry(QtCore.QRect(170, 30, 20, 241))
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))

        self.retranslateUi(SegmenationMetrics)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SegmenationMetrics.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SegmenationMetrics.reject)
        QtCore.QMetaObject.connectSlotsByName(SegmenationMetrics)

    def retranslateUi(self, SegmenationMetrics):
        SegmenationMetrics.setWindowTitle(_translate("SegmenationMetrics", "Dialog", None))
        self.area_check.setText(_translate("SegmenationMetrics", "Area", None))
        self.circularity_check.setText(_translate("SegmenationMetrics", "Circularity", None))
        self.intensity_check.setText(_translate("SegmenationMetrics", "Colour intensity", None))
        self.angle_check.setText(_translate("SegmenationMetrics", "Gamma and angle", None))
        self.directionality_check.setText(_translate("SegmenationMetrics", "Directionality", None))
        self.solidity_check.setText(_translate("SegmenationMetrics", "Solidity", None))
        self.linearity_check.setText(_translate("SegmenationMetrics", "Linearity", None))
        self.convergence_check.setText(_translate("SegmenationMetrics", "Convergence", None))
        self.distribution_check.setText(_translate("SegmenationMetrics", "Distribution of Elements", None))
        self.label.setText(_translate("SegmenationMetrics", "Pattern Metrics", None))
        self.label_2.setText(_translate("SegmenationMetrics", "Annotations", None))
        self.label_3.setText(_translate("SegmenationMetrics", "Scale", None))
        self.label_4.setText(_translate("SegmenationMetrics", "Scale", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SegmenationMetrics = QtGui.QDialog()
    ui = Ui_SegmenationMetrics()
    ui.setupUi(SegmenationMetrics)
    SegmenationMetrics.show()
    sys.exit(app.exec_())

