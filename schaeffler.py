# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt

aws_e309 = {'name': "AWS E309", 'type': "Eletrodo Austenítico", 'C': 0.200, 'Cu': 0.750, 'Cr': 24.000, 'Mn': 1.750, 'Mo': 0.750, 'Ni': 13.000, 'N': 0.000, 'Si':0.475, 'Others': 0.000}
aisi_316L = {'name': "AISI 316L", 'type': "Austenítico", 'C': 0.030, 'Cu': 0.000, 'Cr': 17.000, 'Mn': 2.000, 'Mo': 2.500, 'Ni': 12.000, 'N': 0.000, 'Si':1.000, 'Others': 0.000}

class Schaeffler:
    """ Class to calculate and generate Schaeffler Diagrams """
    def __init__(self, mb, ma, dilution=0.3):
        self.mb = mb
        self.ma = ma
        self.dilution = dilution
        # Lines of the diagram [(x0,y0), (x1, y1)]
        self.sf_lines = [[(3.1, 0), (0, 8.1)], [(20.46, 2.76), (0, 20.06)], [(12.23, 0), (40, 9.17)],\
         [(6.96, 0), (34.65, 30)], [(26.37, 4.70), (0, 25.73)], [(15.06, 7.34), (37.52, 30)],\
         [(15.82, 6.72), (40.0, 28.38)], [(16.68, 5.97), (40, 23.45)], [(17.74, 5.08), (40, 19.84)], [(18.64, 4.33), (40, 14.53)]]
        # Labels for the lines and regions [(x,y), "Label", fontsize]
        self.sf_labels = [[0.1, 1, "M+F", 9], [31.5, 28, "0%", 9], [31.5, 22.5, "5%", 9], [31.5, 26, "10%", 9],\
         [31.5, 19, "20%", 9], [31.5, 16, "40%", 9], [31.5, 12, "80%", 9], [31.5, 7.5, "100% F", 9],\
         [3, 7, "Martensita", 10], [11, 2, "M+F", 10], [14, 24, "Austenita", 10], [16, 7.5, "A+M+F", 10]]

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
        plot = Plot(creq, nieq, self.sf_lines, self.sf_labels)
        plot.create_plot(weld)

class Plot:
    def __init__(self, creq, nieq, sf_lines, sf_labels):
        # Load Graph BKG
        self.creq = creq
        self.nieq = nieq
        self.fig, self.ax = plt.subplots()
        self.sf_lines = sf_lines
        self.sf_labels = sf_labels

    def create_plot(self, weld, show_lines=True, show_lines_labels=True):
        # Set plt params
        self.ax.grid(b=True, which='major')
        plt.axis('scaled')
        self.ax.set(xlim=(0, 40), ylim=(0, 30), xlabel='Cromo Equivalente (%)', ylabel='Níquel Equivalente (%)', title="Diagrama de Schaeffler")
        
        # Create background lines
        if show_lines:
            # Create a mplib collections from the lines points
            lc = matplotlib.collections.LineCollection(self.sf_lines, colors='k', linewidths=1)
            self.ax.add_collection(lc)
        if show_lines_labels:
            for i, value in enumerate(self.sf_labels, 0):
                # Add labels
                plt.text(value[0], value[1], value[2], fontsize=value[3])
        
        self.ax.plot(self.creq[0], self.nieq[0], 'b<', label="Metal de Base")
        self.ax.plot(self.creq[1], self.nieq[1], 'b>', label="Metal de Adição")
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