# main.py
import sys
import os
import json
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QSplitter, QDialog, QLabel, QVBoxLayout, \
    QPlainTextEdit, QLineEdit, QGridLayout, QWidget, QPushButton, QMessageBox

# from pymarkup_fns import read_csv, read_toml, merge, render_html, render_pdf, load_css, get_subitems, printdic, read_csv_adv, get_images

# import markdown2
# import simpleeval

PATH_SETTINGS = 'settings.json'






'''
class SettingsDialog(QDialog):
    def __init__(self,mw):
        super().__init__()

        self.mw = mw
        # self.setWindowIcon(mw.icon)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Impostazioni')

        self.setup_layout()


    def FilePicker(self,key):
        print('FilePicker',key)
        chosen_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Seleziona file', '', '*.csv',)
        # print(type(chosen_path),chosen_path)
        if chosen_path[0] != '':
            self.widgets[key].setText(chosen_path[0])
            self.mw.settings['paths'][key] = chosen_path[0]


    def FolderPicker(self,key):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Seleziona cartella')
        print(type(chosen_path),chosen_path)
        if chosen_path != '':
            self.widgets[key].setText(chosen_path)
            self.mw.settings['paths'][key] = chosen_path


    def setup_widgets(self):
        pass


    def setup_layout(self):
        # print('Setting up settings dialog UI')

        self.widgets = {
            'table_products':   QLineEdit(),
            'table_macros':     QLineEdit(),
            'img_folder':              QLineEdit(), # QPlainTextEdit()
        }

        widget_labels = {
            'table_products':   "Tabella prodotti:",
            'table_macros':     "Tabella note:",
            'img_folder':              "Cartella immagini:",
        }

        widget_button_slots = {
            'table_products':   lambda: self.FilePicker('table_products'),
            'table_macros':     lambda: self.FilePicker('table_macros'),
            'img_folder':              lambda: self.FolderPicker('img_folder'),
        }

        grid_layout = QGridLayout()

        for i,key in enumerate(self.widgets.keys()):
            label = QLabel(widget_labels[key])
            widget = self.widgets[key]
            widget.setReadOnly(True)
            widget.setDisabled(True)
            button = QPushButton('Seleziona')
            button.pressed.connect(widget_button_slots[key])

            last_used_path = self.mw.settings['paths'].get(key,'')
            if os.path.exists(last_used_path):
                widget.setText(last_used_path)

            grid_layout.addWidget(label,i,0,1,1)
            grid_layout.addWidget(widget,i,1,1,1)
            grid_layout.addWidget(button,i,2,1,1)


        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(grid_widget)
        main_layout.addStretch()
        self.setLayout(main_layout)

        # settings_wh = self.mw.settings.get('settings_wh')
        # if settings_wh is not None:
        geometry = self.mw.settings.get('geometry_wh')
        if geometry:

            x,y,w,h = geometry
            # w,h = settings_wh
            # Position dialog at the center of the main window
            # g = self.mw.geometry()
            # x = g.x() + (g.width()-w) / 2
            # y = g.y() + (g.height()-h) / 2

            # self.setGeometry(x,y,w,h)
        else:
            self.resize(400,500)
'''


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.BASE_TITLE = 'PyQt5 Starter'
        self.setWindowTitle(self.BASE_TITLE)

        # self.settings = self.LoadSettings()
        
        self.init_layout()


    def init_mainmenu(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        # viewmenu = menubar.addMenu('Visualizza')
        
        items_filemenu = [
            ['Nuovo file', 'Ctrl+N', self.Dummy],
            ['Apri...', 'Ctrl+O', self.Dummy],
            ['Salva', 'Ctrl+S', self.Dummy],
            ['Salva con nome...', 'Ctrl+Shift+S', self.Dummy],
            [],
            ['Impostazioni...', 'Ctrl+I',          self.Dummy],
            [],
            ['Chiudi', 'Ctrl+Shift+Q',          self.Dummy],
        ]

        for data in items_filemenu:
            if len(data)>0:
                label,shortcut,function = data
                new_action = QAction(label,self)
                new_action.setShortcut(shortcut)
                new_action.triggered.connect(function)
                filemenu.addAction(new_action)
            else:
                filemenu.addSeparator()


    def init_layout(self):
        
        label1 = QLabel("QLabel 1")
        label2 = QLabel("QLabel 2")
        label3 = QLabel("QLabel 3")
        label4 = QLabel("QLabel 3")
        '''
        grid_layout = QGridLayout()
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        grid_layout.addWidget(label1,0,0,1,1)
        grid_layout.addWidget(label2,0,1,1,1)
        grid_layout.addWidget(label3,1,0,1,1)
        grid_layout.addWidget(label4,0,1,1,1)
        '''
        main_layout = QVBoxLayout()

        main_layout.addWidget(label1)
        main_layout.addWidget(label2)
        main_layout.addWidget(label3)
        main_layout.addWidget(label4)

        # main_layout.addWidget(grid_widget)
        main_layout.addStretch()

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(main_layout)
        self.setCentralWidget(centralWidget)


    def Dummy(self):
        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    main()
