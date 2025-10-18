from models.ModelBallMill import ModelBallMill
from utils.DataToCSV import DataToCSV
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv 


class Perovskites():
    def __init__(self):
        self.MBM = ModelBallMill()
        self.DTC = DataToCSV()#self.MBM)

    def grams_salts(self, mmol, Cl, Br, I, f, Print = True):
        g = self.MBM.calc_precursor_g_mol(mmol, Cl, Br, I)
        e = self.MBM.calculate_e(mmol, Cl, Br, I)
        t = e / (0.01205 * f ** 3) / 60

        if Print:
            if Cl > 0:
                print(f"Choride salts required for {mmol} mmol at {Cl*100} % of total moles")
                print(f"DabcoCl2: {g[0]:.4f} g, NH4Cl: {g[3]:.4f} g")
            if Br > 0:
                print(f"Bromide salts required for {mmol} mmol at {Br*100} % of total moles")
                print(f"DabcoBr2: {g[1]:.4f} g, NH4Br: {g[4]:.4f} g")
            if I > 0:
                print(f"Iodide salts required for {mmol} mmol at {I*100} % of total moles")
                print(f"DabcoI2: {g[2]:.4f} g, NH4I: {g[5]:.4f} g")
            
            print(f"Total Reaction Energy = {e/1000:.4f} KJ. \n"
                   f"Calculated milling time in minutes {t:.2f} \n.")
            
    def generate_csv_precursors(self):#, mmol, Cl, Br, I):
        g = np.around(self.MBM.calc_precursor_g_mol(3, 0.5, 0.0, 0.5), 4)
        n = 6
        test_list = np.empty((6, 10))#, dtype=object)
        
        for i in range(n):
            mole_fracs = np.array([0.5, 0, 0.5])
            row = np.hstack((3, mole_fracs, g))
            test_list[i] = row

        colnames = [
                "mmol", "Frac Cl",  "Frac Br",  "Frac I",  "DabcoCl2 (g)", 
                "DabcoBr2 (g)", "DabcoI (g)", "NH4Cl (g)", "NH4Br (g)", "NH4I (g)"
            ]
        
        print()
        df = pd.DataFrame(test_list, columns = colnames)
        df.to_csv("Data/test.csv", sep = ";", index = False)

    def write_precursor_row(self, mmol, Cl, Br, I):
        g = self.MBM.calc_precursor_g_mol(mmol, Cl, Br, I)
        mole_fracs = np.array([Cl, Br, I])
        row = np.around(np.hstack((3, mole_fracs, g)), 4)
        self.DTC.write_row_csv(row)

    # def write_row_csv(self, dat):
    #     with open('data/test.csv', 'a') as f_object:
    #         writer_object = csv.writer(f_object)
    #         writer_object.writerow(dat)
    #         f_object.close()
  

if __name__ == '__main__':
    ps = Perovskites()
    #ps.grams_salts(3, 0.5, 0.0, 0.5, 20, True)
    ps.DTC.create_CSV()
    ps.write_precursor_row(3, 0.5, 0.0, 0.5)
    #p.generate_csv_precursors()

    pass
