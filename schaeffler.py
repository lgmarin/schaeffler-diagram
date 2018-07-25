# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

aws_e309 = {'name': "AWS E309", 'type': "Eletrodo Austenítico", 'C': 0.200, 'Cu': 0.750, 'Cr': 24.000, 'Mn': 1.750, 'Mo': 0.750, 'Ni': 13.000, 'N': 0.000, 'Si':0.475, 'Others': 0.000}
aisi_316L = {'name': "AISI 316L", 'type': "Austenítico", 'C': 0.030, 'Cu': 0.000, 'Cr': 17.000, 'Mn': 2.000, 'Mo': 2.500, 'Ni': 12.000, 'N': 0.000, 'Si':1.000, 'Others': 0.000}

class Schaeffler:
    def __init__(self, mb, ma, dilution=0.3):
        self.mb = mb
        self.ma = ma
        self.dilution = dilution

    def calc_creq(self, material):
        creq = material['Cr'] + material['Mo'] + 1.5 * material['Si'] + 0.5 * material['Others']
        return creq

    def calc_nieq(self, material):
        nieq = material['Ni'] + 30 * material['C'] + 0.5 * material['Mn']
        return nieq

    def calc_weld(self):
        mb_creq = self.calc_creq(self.mb)
        mb_nieq = self.calc_creq(self.mb)
        ma_creq = self.calc_nieq(self.ma)
        ma_nieq = self.calc_nieq(self.ma)
        creq_weld = self.dilution*mb_creq + (1-self.dilution)*ma_creq
        nieq_weld = self.dilution*mb_nieq + (1-self.dilution)*ma_nieq
        return [creq_weld, nieq_weld]

    def weld(self):
        creq = [self.calc_creq(self.mb), self.calc_creq(self.ma)]
        nieq = [self.calc_nieq(self.mb), self.calc_nieq(self.ma)]
        weld = self.calc_weld()
        # Base Metal
        print("Metal de Base: {0}, Creq: {1:.1f}%, Nieq: {2:.1f}%, Tipo: {3}".format(aisi_316L['name'], creq[0], nieq[0], aisi_316L['type']))
        # Filler Metal
        print("Metal de Adição: {0}, Creq: {1:.1f}%, Nieq: {2:.1f}%, Tipo: {3}".format(aws_e309['name'], creq[1], nieq[1], aws_e309['type'])) 
        # Weld Metal (Welded Joint)
        print("Junta soldada: Creq: {0:.1f}%, Nieq: {1:.1f}%".format(weld[0], weld[1]))
        plot = Plot(creq, nieq)
        plot.create_plot(weld)

class Plot:
    def __init__(self, creq, nieq):
        # Load Graph BKG
        self.creq = creq
        self.nieq = nieq
        self.img = plt.imread("schaeffler_nogrid_2x.png")
        self.fig, self.ax = plt.subplots()

    def create_plot(self, weld):
        self.ax.imshow(self.img, extent=[0, 40, 0, 30])
        self.ax.grid(color='k', linestyle='--', linewidth=1)
        self.ax.plot(self.creq[0], self.nieq[0], 'b<', label="Metal de Base")
        self.ax.plot(self.creq[1], self.nieq[1], 'b>', label="Metal de Adição")
        self.ax.set(xlabel='Cromo Equivalente (%)', ylabel='Níquel Equivalente (%)', title="Diagrama de Schaeffler")
        self.ax.plot(weld[0], weld[1], 'bo', label="Solda")
        plt.show()

    def add_plot(self, weld):
        self.ax.plot(weld[0], weld[1], 'bo', label="Solda")
        plt.show()
        
    def save_plot(self):
        self.fig.savefig("test.png", format='png', dpi=600, bbox_inches='tight')

if __name__ == '__main__':
    app = Schaeffler(aisi_316L, aws_e309, 0.3)
    app.weld()