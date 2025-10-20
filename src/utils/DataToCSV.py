import numpy as np
from csv import writer
import pandas as pd
from pathlib import Path

class DataToCSV:
    def __init__(self):#, MBM):
        #self.MBM = MBM
        self.col_labels_prec = [
                "mmol", "Frac Cl",  "Frac Br",  "Frac I",  "D-HCl2(g)", 
                "D-HBr2(g)", "D-HI2(g)", "NH4Cl(g)", "NH4Br(g)", "NH4I(g)"]
            #     "20hz_mn", "25hz_mn", "30hz_mn"
            # ]
        
        self.col_labels_timefreq = [
            "mmol", "Cl",  "Br",  "I", "20hz_mn", "21hz_mn", "22hz_mn", "23hz_mn", 
            "24hz_mn", "25hz_mn", "26hz_mn", "27hz_mn", "28hz_mn", "29hz_mn", "30hz_mn"
        ]
    

    def create_CSV(self, col_labels = None, check = True, filename = "data.csv"):
        if check:
            new_filename = self.check_csv_exists(filename)
            filename = new_filename

        if col_labels is None:
            col_labels = self.col_labels_prec
        
        csv_df = pd.DataFrame(columns = col_labels)
        csv_df.to_csv(f"Data/{filename}", sep = ";", index = False)

        return filename


    def write_row_csv(self, dat, filename = "test2.csv" ):
    
        with open(f'data/{filename}', 'a', newline='') as f_object:
            writer_object = writer(f_object, delimiter=";")
            writer_object.writerow(dat)
            f_object.close()


    def write_rows_csv(self, data, filename = "test2.csv"):

        with open(f'data/{filename}', 'a', newline='') as f_object:
            for line in data:
                writer_object = writer(f_object, delimiter=";")
                writer_object.writerow(line)
            f_object.close()


    def check_csv_exists(self, filename = str):
        file = Path(f"../src/data/{filename}") 
        
        if not file.is_file():
            return filename
        
        fp = filename
        i = 1

        while file.is_file():
            split = fp.split('.')
            new_filename = f'{split[0]}({i}).{split[1]}'
            file = Path(f"../src/data/{new_filename}") 
            i += 1
        
        return new_filename
            
    def read_csv(self):
        pass
  
if __name__ == '__main__':
    pass

