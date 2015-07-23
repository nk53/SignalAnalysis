


#creating a tabbed interface:
#http://ubuntuforums.org/showthread.php?t=1144712 
import sys, os.path, inspect
import pandas as pd

from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc
from PyQt4.QtCore import pyqtSlot as qtslot


class Example(qtg.QWidget):

    def __init__(self, width=300, height=300):
        super(Example, self).__init__()
        
        self.curr_dir = os.path.expanduser("~")
        self.openicon = qtg.QIcon("pics/open_folder.png") #'file dialog' icon
        #self.filepath = "/Users/morganfine-morris/test/t_vals from 2way ANOVA of Peaks per Burst.csv"
        self.sep = " " #temporarily set to "," until separators section works

        self.initUI(width, height)
        
        
    def open_file_dialog(self):
        """"Get the name of the file to import.
            Set the output_dir to the file dir by default
            TODO: error catching. maybe set a current_directory flag here?
        """
        
        filepath  = qtg.QFileDialog.getOpenFileName(self, "Choose Data File", self.curr_dir)
            
        if filepath:
            self.filepath = filepath
            self.input_datapath.setText(self.filepath)
            try:
                self.curr_dir = os.path.dirname(str(self.filepath))
                self.output_datapath.setText(self.curr_dir)
            except Exception as e:
                print e
                pass #what should go here?
                
            self.load_file_preview()

        
    def open_dir_dialog(self):
        """Get the name of the folder where files output by the program
        should be saved."""
            
        directory = qtg.QFileDialog.getExistingDirectory(self, "Choose Output Directory", self.curr_dir)
        if directory:
            self.output_directory = directory
            self.curr_dir = directory
            self.output_datapath.setText(self.output_directory)
        
    def set_sep(self):
        print self.btn_group.checkedButton()
    
    
    def _map_dataframe_to_QTableWidget(self, dataframe, qt_table):
        """"generalized so that it can be used with any QTableWidget"""
        
        collabels = dataframe.columns
        rowlabels = dataframe.index
        
        #for column with row labels
        #iterate thru the rows of the column and add info to col 0
        for n, row in enumerate(rowlabels, start=1):
            qt_table.setItem(n, 0, qtg.QTableWidgetItem(str(row)))

        #for each column in table
        #get column name. get column data
        #iterate thru the rows of the column and add info
        for n, col in enumerate(collabels, start=1):
            qt_table.setItem(0, n, qtg.QTableWidgetItem(str(col)))
            for ne, elem in enumerate(dataframe[col], start=1):
                qt_table.setItem(ne, n, qtg.QTableWidgetItem(str(elem)))

    
    def from_csv(self):
        """
        modified from answer to stackoverflow question 10636024
        answer provided by user1319128 at Aug 20 '12 at 11:30 
        edited by Rostyslav Dzinko at Aug 20 '12 at 13:28 
        """
        numrows = 5
        if not (self.filepath and self.sep):
            print "fail to display table."
        
        df  = pd.read_table(str(self.filepath), sep=self.sep, index_col = 0, header = 0, nrows=numrows)

        #add 1 to both column and row count to include row and column labels
        self.preview_table.setColumnCount(len(df.columns))
        self.preview_table.setRowCount(len(df.index))
        
        self._map_dataframe_to_QTableWidget(df, self.preview_table)
        
        
    def load_file_preview(self):
    
        numrows = 5
        if not (self.filepath and self.sep):
            print "failed to display table."
            
        #open file, read lines, split by delimiter
        all_lines = []
        with open(self.filepath) as f:
        
            for n, line in enumerate(f):
                if n >= numrows:
                    break
                
                elements = line.strip().split(self.sep)
                all_lines.append(elements)
        
        # determine max row length
        # set row and column count
        max_line_len = max(map(len, all_lines))    
        self.preview_table.setColumnCount(max_line_len)
        self.preview_table.setRowCount(numrows)        
        
        for n, line in enumerate(all_lines):
            for nn, element in enumerate(line):
                item = qtg.QTableWidgetItem(str(element))
                self.preview_table.setItem(n, nn, item)
        
        
        
            
            


    def initUI(self, width, height):
        #setup and show window
        self.setGeometry(0, 0, width, height)
        self.setMinimumSize(500,650)
        self.center()
        self.setWindowTitle("Signal Analysis") #once a file has been imported, change the name
        #self.setWindowIcon(qtg.QIcon("pics/signal2_temp.png"))#"pics/thicklines.png"))
    
        """
        exitAction = qtg.QAction(qtg.QIcon("exit.png"), "&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(qtg.qApp.quit)
        
        #menu bar
        menubar = qtg.QMenuBar()
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
        tabs_widg = qtg.QTabWidget(self)
        load_tab = qtg.QWidget()
        eventdet_tab = qtg.QWidget()
        postdet_tab = qtg.QWidget()
        analysis_tab = qtg.QWidget()
        
        # Add tabs to tabs_widg
        tabs_widg.addTab(load_tab,"&Load Data")
        tabs_widg.addTab(eventdet_tab,"&Event Detect")
        tabs_widg.addTab(postdet_tab,"&Post Detection")
        tabs_widg.addTab(analysis_tab,"&Interval Analysis")
        
        
        ########################
        #### LOAD CSVs PAGE ####
        ########################

        load_page = qtg.QVBoxLayout(load_tab) # connects load page and tab
        
        ### Page Components

        ## make and add input file fields
        input_label = qtg.QLabel('Data File:')
        self.input_datapath = qtg.QLineEdit()
        file_dialog_btn = qtg.QPushButton(icon=self.openicon,text="")
        file_dialog_btn.setIconSize(qtc.QSize(20, 20))
        
        inputfile_box = qtg.QHBoxLayout()
        inputfile_box.addWidget(input_label)
        inputfile_box.addWidget(self.input_datapath)
        inputfile_box.addWidget(file_dialog_btn)
        
        ## make and add output folder fields
        output_label = qtg.QLabel('Output Folder:')
        self.output_datapath = qtg.QLineEdit()
        folder_dialog_btn = qtg.QPushButton(icon=self.openicon,text="")
        folder_dialog_btn.setIconSize(qtc.QSize(20, 20))

        outputfolder_box = qtg.QHBoxLayout()
        outputfolder_box.addWidget(output_label)
        outputfolder_box.addWidget(self.output_datapath)
        outputfolder_box.addWidget(folder_dialog_btn)

        #connections
        file_dialog_btn.clicked.connect(self.open_file_dialog)
        
        folder_dialog_btn.clicked.connect(self.open_dir_dialog)
        self.input_datapath.textChanged.connect(self.load_file_preview)
        
        filepath_boxes = qtg.QVBoxLayout()
        filepath_boxes.addLayout(inputfile_box)
        filepath_boxes.addLayout(outputfolder_box)
        
        load_page.addLayout(filepath_boxes)
        
        ## separators
        separators_label = qtg.QLabel('Separators')
        custom_sep_label = qtg.QLabel('custom')

        comma_sep = qtg.QCheckBox('commas', self)
        comma_sep.setChecked(True)
        tab_sep = qtg.QCheckBox('tab', self)
        space_sep = qtg.QCheckBox('space', self)
        custom_sep = qtg.QCheckBox('custom', self)
        custom_text = qtg.QLineEdit('custom', self)
        custom_text.setReadOnly(True) #if custom_sep check, change to false
        self.btn_group = qtg.QButtonGroup()
        self.btn_group.addButton(comma_sep)
        self.btn_group.addButton(tab_sep)
        self.btn_group.addButton(space_sep)
        self.btn_group.addButton(custom_sep)
        #for button in btn_group.buttons:
        #    btn_group.stateChanged.connect(set_sep)

        #btn_group.stateChanged.connect(
        
        separators = qtg.QHBoxLayout()
        separators.addWidget(separators_label)
        separators.addWidget(comma_sep)
        separators.addWidget(tab_sep)
        separators.addWidget(space_sep)
        separators.addWidget(custom_sep)
        separators.addWidget(custom_text)
        
        load_page.addLayout(separators)
        
        # row boundaries, time column
        first_row_label = qtg.QLabel('First Row (include column labels)')
        last_row_label = qtg.QLabel('Last Row')
        first_row = qtg.QSpinBox()
        last_row = qtg.QSpinBox()
        first_row.setWrapping(True)
        last_row.setWrapping(True)
        
        time_col_label = qtg.QLabel('Time Col')
        time_col = qtg.QSpinBox()
        time_col.setWrapping(True)
        
        reset_cols_btn = qtg.QPushButton("&Reset Column Selection")
        row_boundries = qtg.QHBoxLayout()
        row_boundries.addWidget(first_row_label)
        row_boundries.addWidget(first_row)
        row_boundries.addWidget(last_row_label)
        row_boundries.addWidget(last_row)
        row_boundries.addWidget(time_col_label)
        row_boundries.addWidget(time_col)
        row_boundries.addWidget(reset_cols_btn)
        
        load_page.addLayout(row_boundries)

        ## file preview
        file_prev_label = qtg.QLabel('File Preview')
        self.preview_table = qtg.QTableWidget(self)
                
        table_box = qtg.QVBoxLayout()
        table_box.addWidget(file_prev_label)
        table_box.addWidget(self.preview_table)
        load_page.addLayout(table_box)

        
        #fill up any remaining space
        load_page.addStretch(1)
        
        
        #set layout
        vbox = qtg.QVBoxLayout()
        #vbox.addWidget(menubar)
        vbox.addWidget(tabs_widg)
        self.setLayout(vbox)
        
    def center(self):
        screen = qtg.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2) 
        
        

def main():
    
    app = qtg.QApplication(sys.argv)
    #app.setStyle("plastique")
    
    #d = qtg.QFileDialog()
    #d.show()
    
    ex = Example(800,800) 
    #ex.from_csv()#load_file_preview()
    #ex.load_file_preview()

    ex.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()