
"""
what sorts of settings/preferences might I provide?
-initial (default) directory file dialogs open in
-should file dialogs remember the last visited directory, or always open to default 
-autosave on/off
-default separator type
-default comment type


on csv import tab, table preview:
-can I make multiple different selections with diff colors?
-can I differentiate between selections made by clicking and selections made programmatically?
-how to I change a column, row, or cells background color?


doc string formatting:
http://sphinx-doc.org/latest/ext/napoleon.html
http://google.github.io/styleguide/pyguide.html#Comments
"""

#creating a tabbed interface:
#http://ubuntuforums.org/showthread.php?t=1144712 
import sys, os.path, inspect
import pandas as pd

from PyQt4 import QtGui as qtg
from PyQt4 import QtCore as qtc
from PyQt4.QtCore import pyqtSlot as qtslot
from TabulatedDataImporterWidget import TabulatedDataImporterWidget as Importer

class Example(qtg.QWidget):

    def __init__(self, width=300, height=300):
        super(Example, self).__init__()
        
        self.delimiter_name_symb = {"comma":",", "space": " ", "tab": "\t"}
        self.filepath = "/Users/morganfine-morris/test/t_vals from 2way ANOVA of Peaks per Burst.csv" #test file
        self.curr_dir = os.path.expanduser("~")
        self.sep = "," #temporarily set to "," until separators section works
        
        ## icons
        self.openicon = qtg.QIcon("pics/open_folder.png") #'file dialog' icon

        self.initUI(width, height)
            
    def error_dialog(self, exception):
        title_str = str(type(exception))
        err_dialog = qtg.QMessageBox(text=exception.message, parent=self)
        err_dialog.setStandardButtons(qtg.QMessageBox.Close)
        err_dialog.show()
        #close = qtg.QPushButton(text="C&lose", parent=err_dialog)
        #err_dialog.addButton(close, 0)
        #close.clicked.connect(err_dialog.closeEvent)  
            
    def initUI(self, width, height):
        #setup and show window
        self.setGeometry(0, 0, width, height)
        self.setMinimumSize(500,500)
        self.center()
        self.setWindowTitle("Signal Analysis") #once a file has been imported, change the name
            
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
        
        importer = Importer()
        load_page.addWidget(importer)
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
        
        
    ''' 
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
    '''
        

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