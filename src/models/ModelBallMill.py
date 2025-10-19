import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ModelBallMill:
    def __init__(self, SI = False):

        self.SI = SI
        self.SI_conv_factor = 1 if not self.SI else 10 ** -3
        self.SI_t_SI = 60 if not SI else 1
        self.Na = 6.0331408 * 10 ** 23

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
        self.DacoHCl2 = 0.9250 / 5  * self.SI_conv_factor
        self.DacoHBr2 = 0.822 / 3 * self.SI_conv_factor
        self.DacoHI2 = 0.736 / 2  * self.SI_conv_factor

        self.NH4Cl = 0.267 / 5  * self.SI_conv_factor
        self.NH4Br = 0.293 / 3  * self.SI_conv_factor
        self.NH4i= 0.289 / 2  * self.SI_conv_factor

        self.moles = np.array([
                self.DacoHCl2, 
                self.DacoHBr2, 
                self.DacoHI2, 
                self.NH4Cl,
                self.NH4Br,
                self.NH4i
            ])

        #Densities precursors 

        #Densities of precursor not well known DabcoHCl2 has a density of 2.23 g/cm³ at 123K and density given at crystal structure after 265K (-8 C)

        self.rho_DabcoHCl2 = 2.23 / self.SI_conv_factor
        self.rho_DabcoHBr2 = 1 / self.SI_conv_factor
        self.rho_DabcoHI2 = 1  / self.SI_conv_factor

        #1.53 g/cm³at 68F/20C 1.519 in handbook of chem. and phys.
        self.rho_NH4Cl = 1.52 / self.SI_conv_factor
        #2.429 g/cm³ at 25C 
        self.rho_NH4Br = 2.429 / self.SI_conv_factor
        #2.56 at 20 C, 2.514 at 25 C
        self.rho_NH4i= 2.56 / self.SI_conv_factor

        self.densities = np.array([
                self.rho_DabcoHCl2, 
                self.rho_DabcoHBr2, 
                self.rho_DabcoHI2, 
                self.rho_NH4Cl,
                self.rho_NH4Br,
                self.rho_NH4i
            ])

        # Calculate the energy per mmol from the optimized reactions
        self.e_cl = 3.5138 * 10 ** 6 / 5 
        self.e_br = 1.3668 * 10 ** 6 / 3 
        self.e_I = 0.52056 * 10 ** 6 / 2

    def calc_precursor_g_mol(self, mmol, Cl, Br, I):
        g_DabcoCl2 = self.DacoHCl2 * mmol * Cl * self.SI_conv_factor
        g_DabcoBr2 = self.DacoHBr2 * mmol * Br * self.SI_conv_factor
        g_DabcoI2  = self.DacoHI2  * mmol * I * self.SI_conv_factor
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
        t = (e / (0.01205 * f ** 3)) / 60
        return t
    
    def calculate_e(self, mmol, Cl, Br, I):
        e = (self.e_cl * Cl * mmol + self.e_br * Br * mmol + self.e_I * I * mmol) 
        return e
    
    def filling_factor(self, v_jar, grams):
        return (grams / self.densities) / v_jar
    
    def calc_density(self, Z, M, a, b, c):
        return (Z * M) / ((a * b * c) * self.Na)
    
    def calc_ball_weight(self, n, rho, d):
        r = d/2
        m = n * (4 / 3 * np.pi * r ** 3) * rho
        return m    
    
if __name__ == '__main__':
    MBM = ModelBallMill()
    #DabcoHCl2 ρ (g/cm³), note: seems to be a the room temp crystal phase
    str1 = f"DabcoHCl2 ρ [g/cm³]: "
    print(str1, MBM.calc_density(4, 185, 12.88 * 10 ** -8, 7.68 * 10 ** -8, 11.44 * 10 ** -8))
    #NH4+Cl ρ (g/cm³)
    str2 = f"{"NH4+Cl ρ [g/cm³]: ":<25}"
    a = 3.868 * 10 ** -8
    print(MBM.calc_density(4, 53.49, a, a, a))
    #NH4+Br ρ (g/cm³)
    str3 = f"DabcoHCl2 ρ [g/cm³]: "
    a = 6.9 * 10 ** -8
    print(MBM.calc_density(4, 97.94, a, a, a))
    #NH4+I ρ (g/cm³)
    str4 = f"DabcoHCl2 ρ [g/cm³]: "
    a = 7.199 * 10 ** -8
    print(MBM.calc_density(4, 144.943, a, a, a))
    #NH4+Br ρ (g/cm³)

    print(MBM.calc_ball_weight(2, 5.68, 1))

