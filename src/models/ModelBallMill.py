import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ModelBallMill:
    def __init__(self, SI = False):

        self.SI = SI
        self.SI_conv_factor = 1 if not self.SI else 10 ** -3
        self.SI_t_SI = 60 if not SI else 1

        # Milling ball properties
        self.rho_ball = None
        self.r_ball = None
        self.eps_ball = None
        self.poisson_ball = None
        self.n_ball = 1

        self.a = None
        self.m = None
        self.c = None
        self.v_jar = None 

        #Calculating Molar masses (in g/mmol and kg/mol if SI option on)
        self.DabcoCl2 = 0.9250 / 5  * self.SI_conv_factor
        self.DabcoBr2 = 0.822 / 3 * self.SI_conv_factor
        self.DabcoI2 = 0.736 / 2  * self.SI_conv_factor

        self.NH4Cl = 0.267 / 5  * self.SI_conv_factor
        self.NH4Br = 0.293 / 3  * self.SI_conv_factor
        self.NH4i= 0.289 / 2  * self.SI_conv_factor

        self.moles = np.array([
                self.DabcoCl2, 
                self.DabcoBr2, 
                self.DabcoI2, 
                self.NH4Cl,
                self.NH4Br,
                self.NH4i
            ])

        #Densities precursors
        self.rho_DabcoCl2 = 1 # * if not SI else 0.9250 / 5 * 10 ** -3
        self.rho_DabcoBr2 = 1 #if not  SI else 0.822 / 3 * 10 ** -3
        self.rho_DabcoI2 = 1  #if not SI else 0.736 / 2  * 10 ** -3

        self.rho_NH4Cl = 1   #if not SI else 0.267 / 5 * 10 ** -3
        self.rho_NH4Br = 1   #if not SI else 0.293 / 3 * 10 ** -3
        self.rho_NH4i= 1     #if not SI else 0.293 / 3 * 10 ** -3

        self.densities = np.array([
                self.rho_DabcoCl2, 
                self.rho_DabcoBr2, 
                self.rho_DabcoI2, 
                self.rho_NH4Cl,
                self.rho_NH4Br,
                self.rho_NH4i
            ])

        # Calculate the energy per mmol from the optimized reactions
        self.e_cl = 3.5138 * 10 ** 6 / 5 
        self.e_br = 1.3668 * 10 ** 6 / 3 
        self.e_I = 0.52056 * 10 ** 6 / 2

    def calc_precursor_g_mol(self, mmol, Cl, Br, I):
        g_DabcoCl2 = self.DabcoCl2 * mmol * Cl * self.SI_conv_factor
        g_DabcoBr2 = self.DabcoBr2 * mmol * Br * self.SI_conv_factor
        g_DabcoI2  = self.DabcoI2  * mmol * I * self.SI_conv_factor
        g_NH4Cl   = self.NH4Cl * mmol * Cl * self.SI_conv_factor
        g_NH4Br   = self.NH4Br * mmol * Br * self.SI_conv_factor
        g_NH4i    = self.NH4i * mmol * I * self.SI_conv_factor

        return np.array([g_DabcoCl2, g_DabcoBr2, g_DabcoI2 ,g_NH4Cl, g_NH4Br , g_NH4i])
    
    def calc_precursor_g_ff(self, ff, vjar, Cl, Br, I):
        mol_per_ml= (np.array([Cl, Cl, Br, Br, I, I]) * self.densities) / self.moles
        mol_ttl = mol_per_ml * ff * vjar
        return self.calc_precursor_g_mol(mol_ttl, Cl, Br, I)

    def calculate_t(self, mmol, Cl, Br, I, f):
        e = (self.e_cl * Cl * mmol + self.e_br * Br * mmol + self.e_I * I * mmol) 
        t = e / (0.01205 * f ** 3) / self.SI_t_SI 
        return t
    
    def calculate_e(self, mmol, Cl, Br, I):
        e = (self.e_cl * Cl * mmol + self.e_br * Br * mmol + self.e_I * I * mmol) 
        return e
    
    def filling_factor(self, v_jar, grams):
        return (grams / self.densities) / v_jar
    
    # def grams_salts(self, mmol, Cl, Br, I, f, Print = True):

    #     g_DabcoCl2 = self.DabcoCl2 * mmol * Cl
    #     g_DabcoBr2 = self.DabcoBr2 * mmol * Br
    #     g_DabcoI2  = self.DabcoI2  * mmol * I
    #     g_NH4Cl   = self.NH4Cl * mmol * Cl
    #     g_NH4Br   = self.NH4Br * mmol * Br
    #     g_NH4i    = self.NH4i * mmol * I

    #     e = (self.e_cl * Cl * mmol + self.e_br * Br * mmol + self.e_I * I * mmol) 
    #     t = e / (0.01205 * f ** 3) / 60
        
    #     if Print:
    #         if Cl > 0:
    #             print(f"Choride salts required for {mmol} mmol at {Cl*100} % of total moles")
    #             print(f"DabcoCl2: {g_DabcoCl2:.4f} g, NH4Cl: {g_NH4Cl} g")
    #         if Br > 0:
    #             print(f"Bromide salts required for {mmol} mmol at {Br*100} % of total moles")
    #             print(f"DabcoBr2: {g_DabcoBr2:.4f} g, NH4Br: {g_NH4Br} g")
    #         if I > 0:
    #             print(f"Iodide salts required for {mmol} mmol at {I*100} % of total moles")
    #             print(f"DabcoI2: {g_DabcoI2:.4f} g, NH4I: {g_NH4i} g")

    #         print(f"Total Reaction Energy = {e/1000:.4f} KJ.")#\n Calculated milling time in minutes {t:.2f} \n.")
    #     return 

if __name__ == '__main__':
    pass

