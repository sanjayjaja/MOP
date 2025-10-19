from models.ModelBallMill import ModelBallMill
from utils.DataToCSV import DataToCSV
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv 
from pathlib import Path


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

    def write_precursor_row(self, mmol, Cl, Br, I, file_prec = "test2.csv", 
                            file_tfreq = "MillingTimes.csv", T = False):
        
        g = np.around(self.MBM.calc_precursor_g_mol(mmol, Cl, Br, I), 4)
        mole_fracs = np.array([Cl, Br, I])
        
        t20 = self.MBM.calculate_t(mmol, Cl, Br, I, 20)
        t25 = self.MBM.calculate_t(mmol, Cl, Br, I, 25)
        t30 = self.MBM.calculate_t(mmol, Cl, Br, I, 30)
        times = np.around(np.array([t20, t25, t30]), 2)
 
        row = np.hstack((3, mole_fracs, g))#, times))
        self.DTC.write_row_csv(row, file_prec)

        if T:
            #file = Path(f"/data/{file_tfreq}")

            #if not file.is_file():
                #self.DTC.create_CSV(self.DTC.col_labels_timefreq, file_tfreq)

            f_list = np.arange(20, 31)
            t_list = np.around(np.array([
                self.MBM.calculate_t(mmol, Cl, Br, I, f) for f in f_list
                ]), 2)
            
            row = np.hstack((mmol, mole_fracs, t_list))

            self.DTC.write_row_csv(row, file_tfreq)

    def MillingTimesToCsv(self):
        pass


  

if __name__ == '__main__':
    #19-10: Calculations for the first synthesis runs
    ps = Perovskites()

    fp = "PrecursorGrams.csv"
    ft = "MillingTimes.csv"
    T = True

    ps.DTC.create_CSV(ps.DTC.col_labels_prec, fp)
    ps.DTC.create_CSV(ps.DTC.col_labels_timefreq, ft)
    ps.write_precursor_row(3, 0.25, 0.0, 0.75, fp, ft, T)
    ps.write_precursor_row(3, 0.5, 0.0, 0.5  , fp, ft, T)
    ps.write_precursor_row(3, 0.75, 0.0, 0.25, fp, ft, T)
    ps.write_precursor_row(3, 0.25, 0.75, 0.0, fp, ft, T)
    ps.write_precursor_row(3, 0.5, 0.5, 0.0  , fp, ft, T)
    ps.write_precursor_row(3, 0.75, 0.25, 0.0, fp, ft, T)
    ps.write_precursor_row(3, 0.0, 0.25, 0.75, fp, ft, T)
    ps.write_precursor_row(3, 0.0, 0.5, 0.5  , fp, ft, T)
    ps.write_precursor_row(3, 0.0, 0.75, 0.25, fp, ft, T)

