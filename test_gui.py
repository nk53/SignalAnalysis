#creating a tabbed interface:
#http://ubuntuforums.org/showthread.php?t=1144712 
import sys
import inspect
import pandas

from PyQt4 import QtGui as qtGui
from PyQt4 import QtCore as qtCore
from PyQt4.QtCore import pyqtSlot

#undoicon = QIcon.fromTheme("edit-undo")
#self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton)
import os.path
#os.path.expanduser("~") #to get the root
#filename = QFileDialog.getOpenFileName(w, 'Open File', os.path.expanduser("~"))

def 
"""
http://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix
answered Aug 20 '12 at 11:30 by user1319128
"""

df  = read_csv(filename, index_col = 0,header = 0)
self.datatable = QtGui.QTableWidget(parent=self)
self.datatable.setColumnCount(len(df.columns))
self.datatable.setRowCount(len(df.index))
for i in range(len(df.index)):
    for j in range(len(df.columns)):
        self.datatable.setItem(i, j, QtGui.QTableWidgetItem(str(df.iget_value(i, j))))



class Example(qtGui.QWidget):

    def __init__(self, width=300, height=300):
        super(Example, self).__init__()
        
        self.curr_dir = os.path.expanduser("~")
        
        self.initUI(width, height)
        
        
    def open_file_dialog(self):
        """"Get the name of the file to import.
            Set the output_dir to the file dir by default
            TODO: error catching. maybe set a current_directory flag here?
        """
        
        filename  = qtGui.QFileDialog.getOpenFileName(self, "Choose Data File", self.curr_dir)
            
        if filename:
            self.filename = filename
            self.input_datapath.setText(self.filename)
            try:
                self.curr_dir = os.path.dirname(str(self.filename))
                self.output_datapath.setText(self.curr_dir)
            except Exception as e:
                print e
                pass #what should go here?
        
    def open_dir_dialog(self):
        """Get the name of the folder where files output by the program
        should be saved."""
            
        directory = qtGui.QFileDialog.getExistingDirectory(self, "Choose Output Directory", self.curr_dir)
        if directory:
            self.output_directory = directory
            self.curr_dir = directory
            self.output_datapath.setText(self.output_directory)
        
    def load_file_preview(self):
        pass
        
    def set_sep(self):
        print self.btn_group.checkedButton()
    
        
    
    
    def initUI(self, width, height):
        #setup and show window
        self.setGeometry(0, 0, width, height)
        self.setMinimumSize(500,650)
        self.center()
        self.setWindowTitle("Signal Analysis") #once a file has been imported, change the name
        #self.setWindowIcon(qtGui.QIcon("pics/signal2_temp.png"))#"pics/thicklines.png"))
    
        """
        exitAction = qtGui.QAction(qtGui.QIcon("exit.png"), "&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(qtGui.qApp.quit)
        
        #menu bar
        menubar = qtGui.QMenuBar()
        try:
            import platform
            platform.mac_ver() #should fail if not a mac (test this!)
            menubar.setNativeMenuBar(False) #necessary for macs!
        except:
            pass
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(exitAction)
        """
        
        
        #make tabs_widg widget and tabs
        tabs_widg = qtGui.QTabWidget(self)
        load_tab = qtGui.QWidget()
        eventdet_tab = qtGui.QWidget()
        postdet_tab = qtGui.QWidget()
        analysis_tab = qtGui.QWidget()
        
        # Add tabs to tabs_widg
        tabs_widg.addTab(load_tab,"&Load Data")
        tabs_widg.addTab(eventdet_tab,"&Event Detect")
        tabs_widg.addTab(postdet_tab,"&Post Detection")
        tabs_widg.addTab(analysis_tab,"&Interval Analysis")
        
        
        ###################
        #### LOAD CSVs PAGE ####
        load_page = qtGui.QVBoxLayout(load_tab) # connects load page and tab
        
        ### Page Components

        openicon = qtGui.QIcon("pics/open_folder.png") #open file dialog icon

        #input file
        input_label = qtGui.QLabel('Data File:')
        self.input_datapath = qtGui.QLineEdit()
        file_dialog_btn = qtGui.QPushButton(icon=openicon,text="")
        file_dialog_btn.setIconSize(qtCore.QSize(20, 20))
        
        inputfile_box = qtGui.QHBoxLayout()
        inputfile_box.addWidget(input_label)
        inputfile_box.addWidget(self.input_datapath)
        inputfile_box.addWidget(file_dialog_btn)
        
        #output folder
        output_label = qtGui.QLabel('Output Folder:')
        self.output_datapath = qtGui.QLineEdit()
        folder_dialog_btn = qtGui.QPushButton(icon=openicon,text="")
        folder_dialog_btn.setIconSize(qtCore.QSize(20, 20))

        outputfolder_box = qtGui.QHBoxLayout()
        outputfolder_box.addWidget(output_label)
        outputfolder_box.addWidget(self.output_datapath)
        outputfolder_box.addWidget(folder_dialog_btn)

        #connections
        file_dialog_btn.clicked.connect(self.open_file_dialog)
        folder_dialog_btn.clicked.connect(self.open_dir_dialog)
        
        filepath_boxes = qtGui.QVBoxLayout()
        filepath_boxes.addLayout(inputfile_box)
        filepath_boxes.addLayout(outputfolder_box)
        
        '''
        filepath_boxes.addWidget(input_label)
        filepath_boxes.addWidget(self.input_datapath)
        filepath_boxes.addWidget(file_dialog_btn)
        filepath_boxes.addWidget(output_label)
        filepath_boxes.addWidget(self.output_datapath)
        filepath_boxes.addWidget(folder_dialog_btn)
        '''
        load_page.addLayout(filepath_boxes)
        
        # separators
        separators_label = qtGui.QLabel('Separators')
        custom_sep_label = qtGui.QLabel('custom')

        comma_sep = qtGui.QCheckBox('commas', self)
        tab_sep = qtGui.QCheckBox('tab', self)
        space_sep = qtGui.QCheckBox('space', self)
        custom_sep = qtGui.QCheckBox('custom', self)
        custom_text = qtGui.QLineEdit('custom', self)
        custom_text.setReadOnly(True) #if custom_sep check, change to false
        self.btn_group = qtGui.QButtonGroup()
        self.btn_group.addButton(comma_sep)
        self.btn_group.addButton(tab_sep)
        self.btn_group.addButton(space_sep)
        self.btn_group.addButton(custom_sep)
        #for button in btn_group.buttons:
        #    btn_group.stateChanged.connect(set_sep)

        #btn_group.stateChanged.connect(
        
        separators = qtGui.QHBoxLayout()
        separators.addWidget(separators_label)
        separators.addWidget(comma_sep)
        separators.addWidget(tab_sep)
        separators.addWidget(space_sep)
        separators.addWidget(custom_sep)
        separators.addWidget(custom_text)
        
        load_page.addLayout(separators)

        
        # row boundaries, time column
        first_row_label = qtGui.QLabel('First Row (include column labels)')
        last_row_label = qtGui.QLabel('Last Row')
        first_row = qtGui.QSpinBox()
        last_row = qtGui.QSpinBox()
        first_row.setWrapping(True)
        last_row.setWrapping(True)
        
        time_col_label = qtGui.QLabel('Time Col')
        time_col = qtGui.QSpinBox()
        time_col.setWrapping(True)
        
        reset_cols_btn = qtGui.QPushButton("&Reset Column Selection")

        
        row_boundries = qtGui.QHBoxLayout()
        row_boundries.addWidget(first_row_label)
        row_boundries.addWidget(first_row)
        row_boundries.addWidget(last_row_label)
        row_boundries.addWidget(last_row)
        row_boundries.addWidget(time_col_label)
        row_boundries.addWidget(time_col)
        row_boundries.addWidget(reset_cols_btn)

        #row_boundries.addStretch(1)
        
        load_page.addLayout(row_boundries)

        ### file preview
        
        file_prev_label = qtGui.QLabel('File Preview')
        
        model = pandasqt.DataFrameModel()
        table = qtGui.QTableView()
        widget.setModel(model)
        model.setDataFrame(data)
        
        table_box = qtGui.QVBoxLayout()
        table_box.addWidget(file_prev_label)
        table_box.addWidget(table)
        load_page.addLayout(table_box)

        
        #fill up any remaining space
        load_page.addStretch(1)
        
        
        #set layout
        vbox = qtGui.QVBoxLayout()
        #vbox.addWidget(menubar)
        vbox.addWidget(tabs_widg)
        self.setLayout(vbox)
        
    def center(self):
        screen = qtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2) 
        
        

def main():
    
    app = qtGui.QApplication(sys.argv)
    #app.setStyle("plastique")
    
    #d = qtGui.QFileDialog()
    #d.show()
    
    ex = Example(800,800) 
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()