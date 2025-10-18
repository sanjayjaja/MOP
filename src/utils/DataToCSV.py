import numpy as np
from csv import writer
import pandas as pd

class DataToCSV:
    def __init__(self):#, MBM):
        #self.MBM = MBM
        self.col_labels = [
                "mmol", "Frac Cl",  "Frac Br",  "Frac I",  "DabcoCl2 (g)", 
                "DabcoBr2 (g)", "DabcoI (g)", "NH4Cl (g)", "NH4Br (g)", "NH4I (g)"
            ]
        
        pass

    def create_CSV(self, col_labels = None, filename = "test2.csv"):
        if col_labels is None:
            col_labels = self.col_labels
        
        csv_df = pd.DataFrame(columns = col_labels)
        csv_df.to_csv(f"Data/{filename}", sep = ";", index = False)

    def write_row_csv(self, dat, filename = "test2.csv" ):
        with open(f'data/{filename}', 'a') as f_object:
            writer_object = writer(f_object, delimiter=";")
            writer_object.writerow(dat)
            f_object.close()
    
    def read_csv(self):
        pass
  

