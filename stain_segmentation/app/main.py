import sys
from PyQt5 import QtGui, QtWidgets

from generated import main_window, features_dialog, batch_process, batch_process

from .photo_viewer import PhotoViewer
import analysis.stain_segmentation as Seg

import cv2
import os

import time


def image_to_pixmap(image):
    height, width, byteValue = image.shape
    bytesPerLine = byteValue * width

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qImg)    

def select_export_dialog(filename):
    """
    open or create a directory
    """

    dialog = QtWidgets.QFileDialog(None, caption='Export stain analysis')
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog.setDirectory(os.path.dirname(filename))
    dialog.setLabelText(QtWidgets.QFileDialog.Accept, "Export")
    if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
       return dialog.selectedFiles()[0]


class BPA_App(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(BPA_App, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Automated Blood Stain Pattern Analysis - ABPA")
        self.viewer = PhotoViewer(self.centralwidget)
        self.viewer.setMinimumSize(500, 500)
        self.horizontalLayout.addWidget(self.viewer)
        self.actionLoad.triggered.connect(self.load_image)
        self.actionExport.triggered.connect(self.export)
        self.actionSegment_Image.triggered.connect(self.show_metrics)
        self.actionBatch_process.triggered.connect(self.show_batch_dialog)
        self.file_name = ""
        self.folder_name = ''
        self.progressBar.hide()
        self.pixmap = None
        self.result = None
        self.annotations = {}
        self.pattern_metrics = True

        self.pattern = None
        self.scale = 7.0

    def load_image(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            os.path.dirname(self.file_name), "Image files (*.jpg *.gif *.png *.tif)")       

        if file_name:
            self.open_image(file_name)

    def open_image(self, file_name):
        assert os.path.isfile(file_name)

        self.file_name = file_name       
        self.viewer.setPhoto(pixmap=QtGui.QPixmap(self.file_name))
        self.setWindowTitle("ABPA - " + self.file_name)

        self.pattern = None
        self.scale = 7.0


    def export(self):       
        output_path = select_export_dialog(self.file_name)
        if output_path is not None:
            self.progressBar.show()
            self.progressBar.setValue(0)

            Seg.export_pattern(self.pattern, stain_overlay=Seg.draw_stains(self.pattern), output_path=output_path)

            self.progressBar.setValue(100)
            self.progressBar.hide()

    def show_metrics(self):
        if self.file_name != "":
            Dialog = self.show_dialog(features_dialog.Ui_SegmenationMetrics(), self.segment_image)
            Dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "You must load an image first")

    def show_dialog(self, dialog, accept):
        Dialog = QtWidgets.QDialog()
        self.dialog = dialog
        self.dialog.setupUi(Dialog)
        self.dialog.scale_spin.setMinimum(1)
        self.dialog.scale_spin.setValue(self.scale)
        self.dialog.scale_spin.valueChanged.connect(self.update_scale)
        self.dialog.buttonBox.accepted.connect(accept)
        return Dialog

    def update_scale(self, value):
        self.scale = value

    def segment_image(self):
        if self.file_name != "":
            
            self.progressBar.show()
            self.progressBar.setValue(0)
            image = cv2.imread(str(self.file_name))

            self.annotations = {'id': self.dialog.id.isChecked(), 
                        'ellipse': self.dialog.ellipse.isChecked(), 
                        'outline': self.dialog.outline.isChecked(), 
                        'center': self.dialog.center.isChecked(),
                        'directionality': self.dialog.directionality.isChecked(),  
                        'direction_line': self.dialog.direction_line.isChecked(), 
                        'gamma': self.dialog.gamma.isChecked()}
            self.pattern_metrics = {'linearity': self.dialog.linearity_check.isChecked(),
                                    'convergence': self.dialog.convergence_check.isChecked(),
                                    'distribution': self.dialog.distribution_check.isChecked(),
                                    'centroid': self.dialog.centroid_check.isChecked()}
            a = time.time()

            self.pattern = Seg.stain_segmentation(image, self.file_name, scale=self.scale)
           
            print('segment time', time.time() - a)
            self.viewer.setPhoto(pixmap=image_to_pixmap(self.pattern.image))

            self.populate_tables()
            self.viewer.add_annotations(self.annotations, self.pattern)
      
            
    def populate_tables(self):
        self.clear_tables()
        self.populate_stain_table()
        self.populate_pattern_table()
        self.progressBar.setValue(100)
        self.progressBar.hide()

    def populate_stain_table(self):
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setRowCount(len(self.pattern.stains))
        self.tableWidget.itemClicked.connect(self.show_stain)
        headers = ["position x", "position y", "area px", "area_mm", 
                "width ellipse", "height ellipse", "ratio", "angle", "gamma", 
                "direction", "solidity", "circularity", "intensity"]

        self.tableWidget.setHorizontalHeaderLabels(headers)
        ids = [str(i) for i in range(0, len(self.pattern.stains))]
        self.tableWidget.setVerticalHeaderLabels(ids)
        j = 0

        for stain in self.pattern.stains:
            percent = (j / len(self.pattern.stains)) * 50
            self.progressBar.setValue(percent)
            stain_data = stain.get_summary_data()            
            for i in range(1,13):
                if stain_data[i] != None:
                    self.tableWidget.setItem(j,i-1, QtWidgets.QTableWidgetItem(str(stain_data[i])))
            j += 1
        self.tableWidget.show()

    def show_stain(self, item):
        position = (int(self.tableWidget.item(item.row(), 0).text()),
                    int(self.tableWidget.item(item.row(), 1).text()))
        self.viewer.add_rectangle(position[0] - 50, position[1] - 50, 100, 100, str(item.row()))

    def populate_pattern_table(self):
        metrics = ["Linearity - Polyline fit", "R^2", "Distribution - ratio stain number to convex hull area", 
                                "ratio stain area to convex hull area", "Convergence - point of highest density", "box of %60 of intersections", "centroid"]
        self.pattern_table_widget.setColumnCount(2)
        self.pattern_table_widget.setRowCount(len(metrics))
        self.pattern_table_widget.setHorizontalHeaderLabels(["Metric", "Value"])
        pattern_data = self.pattern.get_summary_data(self.pattern_metrics)

        for i in range(len(pattern_data)):
            self.pattern_table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(metrics[i])))
            self.pattern_table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(pattern_data[i])))

    def clear_tables(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clear()
        self.pattern_table_widget.setRowCount(0)
        self.pattern_table_widget.clear()

    def show_batch_dialog(self):   
        self.batch_dialog = batch_process.Ui_BatchProcessing()

        Dialog = self.show_dialog(self.batch_dialog, self.batch_process)
        self.batch_dialog.folder_path.clicked.connect(self.open_folder)
        self.batch_dialog.output_path.clicked.connect(self.output_folder)
        Dialog.exec_()
        
    def open_folder(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', '', options=QtWidgets.QFileDialog.Options())
        self.batch_dialog.folder_path_edit.setText(folder_name)

    def output_folder(self):
        out_folder = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', '', options=QtWidgets.QFileDialog.Options())
        self.batch_dialog.output_path_edit.setText(out_folder)

    def batch_process(self):
        self.progressBar.show()
        self.progressBar.setValue(0)
        folder_name = self.batch_dialog.folder_path_edit.text()
        save_folder = self.batch_dialog.output_path_edit.text()
        scale = self.batch_dialog.scale_spin.value()
        pattern_metrics = dict(
            linearity = self.batch_dialog.linearity_check.isChecked(),
            convergence = self.batch_dialog.convergence_check.isChecked(),
            distribution = self.batch_dialog.distribution_check.isChecked(),
            #centroid = self.batch_dialog.centroid_check.isChecked()
        )

        if folder_name:
            image_files = Seg.find_images(folder_name)
                
            if save_folder == "":
                save_folder = os.path.join(folder_name, "output")

            for i, image_file in enumerate(image_files):
                print(f"Processing image {i}/{len(image_files)}: {image_file}")

                Seg.process_image(image_file, os.path.join(save_folder, os.path.basename(image_file)), scale, pattern_metrics=pattern_metrics)
                self.progressBar.setValue(int(100.0 * (i + 1) / len(image_files)))

            print("Done !")
        
                  


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = BPA_App()

    #file_name="example/#7_cropped_ceiling_panorama.jpg"
    #gui.open_image(file_name)

    gui.show()
    app.exec_()

if __name__ == '__main__':
   main()
