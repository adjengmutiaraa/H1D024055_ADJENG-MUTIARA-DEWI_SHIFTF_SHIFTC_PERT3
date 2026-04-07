# Import library
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

barangterjual = ctrl.Antecedent(np.arange(0, 101, 1), 'barangterjual')
permintaan = ctrl.Antecedent(np.arange(0, 301, 1), 'permintaan')
hargaperitem = ctrl.Antecedent(np.arange(0, 100001, 1), 'hargaperitem')
profit = ctrl.Antecedent(np.arange(0, 4000001, 1), 'profit')
stokmakanan = ctrl.Consequent(np.arange(0, 1001, 1), 'stokmakanan')

# variabel barang terjual
barangterjual['rendah'] = fuzz.trapmf(barangterjual.universe, [0, 0, 0, 40])
barangterjual['sedang'] = fuzz.trimf(barangterjual.universe, [30, 50, 70])
barangterjual['tinggi'] = fuzz.trapmf(barangterjual.universe, [60, 100, 100, 100])

# variabel permintaan
permintaan['rendah'] = fuzz.trapmf(permintaan.universe, [0, 0, 0, 100])
permintaan['sedang'] = fuzz.trimf(permintaan.universe, [50, 150, 250])
permintaan['tinggi'] = fuzz.trapmf(permintaan.universe, [200, 300, 300, 300])

# variabel harga per item
hargaperitem['murah'] = fuzz.trapmf(hargaperitem.universe, [0, 0, 0, 40000])
hargaperitem['sedang'] = fuzz.trimf(hargaperitem.universe, [30000, 50000, 80000])
hargaperitem['mahal'] = fuzz.trapmf(hargaperitem.universe, [60000, 100000, 100000, 100000])

# variabel profit
profit['rendah'] = fuzz.trapmf(profit.universe, [0, 0, 0, 1000000])
profit['sedang'] = fuzz.trimf(profit.universe, [1000000, 2000000, 2500000])
profit['tinggi'] = fuzz.trapmf(profit.universe, [1500000, 2500000, 4000000, 4000000])

# variabel stok makanan
stokmakanan['sedang'] = fuzz.trimf(stokmakanan.universe, [100, 500, 900])
stokmakanan['banyak'] = fuzz.trapmf(stokmakanan.universe, [600, 1000, 1000, 1000])

barangterjual.view()
permintaan.view()
hargaperitem.view()
profit.view()
stokmakanan.view()
input("Tekan ENTER untuk melanjutkan")

# definisi aturan fuzzy
rule1 = ctrl.Rule(barangterjual['tinggi'] & permintaan['tinggi'] & hargaperitem['murah'] & profit['tinggi'], stokmakanan['banyak'])
rule2 = ctrl.Rule(barangterjual['tinggi'] & permintaan['tinggi'] & hargaperitem['murah'] & profit['sedang'], stokmakanan['sedang'])
rule3 = ctrl.Rule(barangterjual['tinggi'] & permintaan['sedang'] & hargaperitem['murah'] & profit['sedang'], stokmakanan['sedang'])
rule4 = ctrl.Rule(barangterjual['sedang'] & permintaan['tinggi'] & hargaperitem['murah'] & profit['sedang'], stokmakanan['sedang'])
rule5 = ctrl.Rule(barangterjual['sedang'] & permintaan['tinggi'] & hargaperitem['murah'] & profit['tinggi'], stokmakanan['banyak'])
rule6 = ctrl.Rule(barangterjual['rendah'] & permintaan['rendah'] & hargaperitem['sedang'] & profit['sedang'], stokmakanan['sedang'])

stok_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
stok_sim = ctrl.ControlSystemSimulation(stok_ctrl)

def prediksi_stok(barang, pmn, harga, prft):
    stok_sim.input['barangterjual'] = barang
    stok_sim.input['permintaan'] = pmn
    stok_sim.input['hargaperitem'] = harga
    stok_sim.input['profit'] = prft

    stok_sim.compute()
    return stok_sim.output['stokmakanan']

if __name__ == '__main__':
    nilai_stok = prediksi_stok(barang=80, pmn=255, harga=25000, prft=3500000)
    print(f"Prediksi stok makanan: {nilai_stok:.2f}")
    stokmakanan.view(sim=stok_sim)
    input("Tekan ENTER untuk melanjutkan")