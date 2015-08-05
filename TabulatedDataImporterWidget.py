import sys, os.path, inspect
import pandas as pd

from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc
from PyQt4.QtCore import pyqtSlot as qtslot


class TabulatedDataImporterWidget(qtg.QWidget):
    def __init__(self, width=300, height=300):
        super(TabulatedDataImporterWidget, self).__init__()

        self.delimiter_name_symb = {"comma":",", "space": " ", "tab": "\t"}
        self.filepath = "/Users/morganfine-morris/test/t_vals from 2way ANOVA of Peaks per Burst.csv" #test file
        self.curr_dir = os.path.expanduser("~")
        self.sep = ","
        self.numrows = 5
        self.row_labels_col = 0
        self.dataframe = None
        
        ## icons
        self.openicon = qtg.QIcon("pics/open_folder.png") #'file dialog' icon
        
        self.initUI()

    def open_file_dialog(self):
        """
        Get the name of the file to import.
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
            
            self.setFocus() 
            self.load_file_preview()
            
            
    def open_dir_dialog(self):
        """
        Get the name of the folder where files output by the program
        should be saved.
        """
        directory = qtg.QFileDialog.getExistingDirectory(self, "Choose Output Directory", self.curr_dir)
        if directory:
            self.output_directory = directory
            self.curr_dir = directory
            self.output_datapath.setText(self.output_directory)
        self.setFocus()
        
    
    def error_dialog(self, exception):
        title_str = str(type(exception))
        err_dialog = qtg.QMessageBox(text=exception.message, parent=self)
        err_dialog.setStandardButtons(qtg.QMessageBox.Close)
        err_dialog.show()
        #close = qtg.QPushButton(text="C&lose", parent=err_dialog)
        #err_dialog.addButton(close, 0)
        #close.clicked.connect(err_dialog.closeEvent)
     
        
    def load_file_preview(self):
        """
        Loads the first numrows of the filepath held in self.filepath, splits them
        by the delimiter contained in self.sep, and enters them into the preview table.
        """
        
        #check for self.filepath
        try:
            if self.filepath == "":
                return 
            elif not os.path.isfile(self.filepath):
                raise IOError("Must specify a valid file.")
        except Exception as e:
            #not sure this part is actually necessary
            self.error_dialog(e)
            return
            
        #open file, read lines        #split lines by delimiter 

        #originally this and the loop below were a single loop
        #I separated them into two, so that I can put them
        #in separate functions later
        all_lines = []
        with open(self.filepath) as f:
        
            for n, line in enumerate(f):
                if n >= self.numrows:
                    break
                try:
                    elements = line.strip().split(self.sep)
                except ValueError:
                    elements = [line.strip()] #empty separator
                all_lines.append(elements)
        
        # determine max row length
        # set row and column count
        max_line_len = max(map(len, all_lines))    
        self.preview_table.setColumnCount(max_line_len)
        
        self.preview_table.setRowCount(self.numrows)     
        
        for n, line in enumerate(all_lines):
            for nn, element in enumerate(line):
                item = qtg.QTableWidgetItem(str(element))
                self.preview_table.setItem(n, nn, item)
                
        self.preview_table.resizeColumnsToContents()
        self.preview_table.resizeRowsToContents()
        self.time_col.setMaximum(max_line_len)
        #self.last_row.setMaximum()
        #self.first_row.setMaximum()

    def get_custom_sep(self):
        self.sep = self.custom_text.text()
        self.load_file_preview()
                
    def handle_sep_buttonpress(self):
        button = self.sep_btns.checkedButton()
        key = str(button.text())
        if key.lower() == "custom":
            #else custom option. process the text box
            #set custom button to on
            self.custom_text.setFocus()
            if self.custom_text.text():
                self.sep = self.custom_text.text()
        else:
            try:
                self.sep = self.delimiter_name_symb[key]
            except:
                return
        self.load_file_preview()
        
    def set_row_labels_col(self):
        self.row_labels_col = self.time_col.value()
        #eventually I will highlight the time column in a different color here
        
        
    def import_file(self):
        self.dataframe  = pd.read_table(str(self.filepath), sep=str(self.sep), index_col = 0, header = 0)        
        print self.dataframe
        
    def initUI(self):
        ## make input file fields
        input_label = qtg.QLabel('Data File:')
        self.input_datapath = qtg.QLineEdit()
        file_dialog_btn = qtg.QPushButton(icon=self.openicon,text="")
        file_dialog_btn.setIconSize(qtc.QSize(20, 20))
        
        ## make output folder fields
        output_label = qtg.QLabel('Output Folder:')
        self.output_datapath = qtg.QLineEdit()
        folder_dialog_btn = qtg.QPushButton(icon=self.openicon,text="")
        folder_dialog_btn.setIconSize(qtc.QSize(20, 20))

        ## connect file dialogs to approp. buttons 
        ## and load preview when input file changes
        file_dialog_btn.clicked.connect(self.open_file_dialog)
        folder_dialog_btn.clicked.connect(self.open_dir_dialog)
        self.input_datapath.textChanged.connect(self.load_file_preview)
        
        ## separators
        separators_label = qtg.QLabel('Delimiters')
        #provided separators
        comma_sep = qtg.QRadioButton('comma', self)
        comma_sep.setChecked(True)
        tab_sep = qtg.QRadioButton('tab', self)
        space_sep = qtg.QRadioButton('space', self)
        custom_sep = qtg.QRadioButton('custom', self)
        #add buttons to group (to make them exclusive)
        self.sep_btns = qtg.QButtonGroup()
        self.sep_btns.addButton(comma_sep)
        self.sep_btns.addButton(tab_sep)
        self.sep_btns.addButton(space_sep)
        self.sep_btns.addButton(custom_sep)
        #misc for custom separator
        custom_sep_label = qtg.QLabel('custom:')
        self.custom_text = qtg.QLineEdit(parent=self)
        self.custom_text.setPlaceholderText('enter custom delimiter symbol')
        
        self.sep_btns.buttonClicked.connect(self.handle_sep_buttonpress)
        #if custom_text is focused on, auto check the custom button
        self.custom_text.textChanged.connect(self.get_custom_sep)
        
        ## file preview
        reset_cols_btn = qtg.QPushButton("R&eset Selected Cols")
        select_all_cols_btn = qtg.QPushButton("S&elect All Cols")
        file_prev_label = qtg.QLabel('File Preview. Select columns to import.')
        self.preview_table = qtg.QTableWidget(self)
        self.preview_table.setSelectionMode(qtg.QAbstractItemView.MultiSelection)
        self.preview_table.setSelectionBehavior(qtg.QAbstractItemView.SelectColumns)
        
        reset_cols_btn.clicked.connect(self.preview_table.clearSelection)
        select_all_cols_btn.clicked.connect(self.preview_table.selectAll)
        
        import_file_btn = qtg.QPushButton(text="I&mport File")
        import_file_btn.clicked.connect(self.import_file)

        ## row boundaries
        first_row_label = qtg.QLabel("First Row (include column labels)")
        last_row_label = qtg.QLabel("Last Row")
        self.first_row = qtg.QSpinBox()
        self.last_row = qtg.QSpinBox()
        self.first_row.setWrapping(True)
        self.last_row.setWrapping(True)
        #self.first_row.valueChanged.connect()
        #self.last_row.valueChanged.connect()
                
        ## make selector for indicating which col is time column
        time_col_label = qtg.QLabel("Time Col")
        time_col_label.setAlignment(qtc.Qt.AlignRight | qtc.Qt.AlignVCenter)
        self.time_col = qtg.QSpinBox()
        self.time_col.setWrapping(True)
        self.time_col.valueChanged.connect(self.set_row_labels_col)

        ##positon elements on load_page tab        
        
        inputfile_box = qtg.QHBoxLayout()
        inputfile_box.addWidget(input_label)
        inputfile_box.addWidget(self.input_datapath)
        inputfile_box.addWidget(file_dialog_btn)
        
        outputfolder_box = qtg.QHBoxLayout()
        outputfolder_box.addWidget(output_label)
        outputfolder_box.addWidget(self.output_datapath)
        outputfolder_box.addWidget(folder_dialog_btn)

        filepath_boxes = qtg.QVBoxLayout()
        filepath_boxes.addLayout(inputfile_box)
        #filepath_boxes.addLayout(outputfolder_box)
        
        separators = qtg.QHBoxLayout()
        separators.addWidget(separators_label)
        separators.addWidget(comma_sep)
        separators.addWidget(tab_sep)
        separators.addWidget(space_sep)
        separators.addWidget(custom_sep)
        separators.addWidget(self.custom_text)

        #row_boundries = qtg.QHBoxLayout()
        #row_boundries.addWidget(first_row_label)
        #row_boundries.addWidget(self.first_row)
        #row_boundries.addWidget(last_row_label)
        #row_boundries.addWidget(self.last_row)
        
        table_box = qtg.QVBoxLayout()
        temp = qtg.QHBoxLayout()
        temp.addWidget(file_prev_label)
        temp.addWidget(reset_cols_btn)
        temp.addWidget(select_all_cols_btn)
        temp.addWidget(time_col_label)
        temp.addWidget(self.time_col)  
        table_box.addLayout(temp)
        table_box.addWidget(self.preview_table)
        
        main_window = qtg.QVBoxLayout(self)

        #add all boxes to main_window
        main_window.addLayout(filepath_boxes)
        main_window.addLayout(separators)
        main_window.addLayout(table_box)
        main_window.addWidget(import_file_btn)
        
        main_window.addLayout(outputfolder_box)
        #main_window.addLayout(row_boundries)
        main_window.addStretch(1)
        
def main():
    
    app = qtg.QApplication(sys.argv)
    
    ex = TabulatedDataImporterWidget() 
    ex.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()