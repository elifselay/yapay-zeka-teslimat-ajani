"""Çatalca merkez teslimat ajanı: bütün sonuçları üretir.
Çalıştırmak için: python calistir.py  (teslimat.py, noktalar.csv, yollar.csv aynı klasörde olmalı)"""
from teslimat import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OGRENCI_NO = 2322120080
DEPO = "Depo_Makrolog"
ADRESLER = ["DevletHastanesi", "YasamVadisi", "YuzuncuYilParki", "ZeytinCafe",
            "DogaRestaurant", "BogaSteakhouse", "KahveTutkusu", "MissBurger"]

N = noktalari_oku("noktalar.csv")
H = yollari_oku("yollar.csv")

# 1) Örnekşehir testi
O = yollari_oku("ornek_yollar.csv")
oh = {"S": 15, "A": 13, "B": 11, "C": 9, "D": 7, "E": 5, "F": 3, "G": 0}
print("=== Örnekşehir testi ===")
for ad, h in [("A*, h=kuş uçuşu", oh), ("A*, h=0", None)]:
    r, km, s = a_yildiz(O, "S", "G", h)
    print(f"{ad:18} {'-'.join(r)}  {km:g} km  açılma: {' '.join(s)} ({len(s)} düğüm)")

# 2) A*: depodan her adrese, gerçek h ve h=0
print("\n=== A* sonuçları (depo -> adres) ===")
print(f"{'Adres':22}{'km':>7}{'Açılan (h)':>12}{'Açılan (h=0)':>14}  Yol")
for a in ADRESLER:
    r, km, s = a_yildiz(H, DEPO, a, kus_ucusu_h(N, a))
    _, _, s0 = a_yildiz(H, DEPO, a)
    print(f"{a:22}{km:7.2f}{len(s):12}{len(s0):14}  {' - '.join(r)}")

# 3) 36 çiftin mesafesi (A* ile) ve genetik algoritma deneyi
d = mesafe_tablosu(H, [DEPO] + ADRESLER, h_fonk=lambda hedef: kus_ucusu_h(N, hedef))
opt_tur, opt_km = kaba_kuvvet(DEPO, ADRESLER, d)

print("\n=== Genetik algoritma deneyi (10 çalıştırma) ===")
sonuc = {}
for pm in (0.1, 0.0):
    kms = []
    for i in range(10):
        tur, km, _, _ = genetik_algoritma(DEPO, ADRESLER, d, pm=pm, seed=OGRENCI_NO + i)
        kms.append(km)
    sonuc[pm] = kms
    print(f"pm={pm}: " + ", ".join(f"{k:.2f}" for k in kms))
    print(f"   en iyi {min(kms):.2f} km · ortalama {sum(kms)/10:.2f} km · "
          f"optimuma ulaşan {sum(abs(k-opt_km) < 1e-9 for k in kms)}/10")

print(f"\nEk puan · kaba kuvvet optimumu: {opt_km:.2f} km  {' - '.join(opt_tur)}")

# 4) Nesle göre grafik (ilk seed)
tur, km, en_iyi, ort = genetik_algoritma(DEPO, ADRESLER, d, seed=OGRENCI_NO)
print(f"Grafikteki çalıştırmanın turu: {' - '.join(tur)} = {km:.2f} km")
plt.figure(figsize=(7, 4))
plt.plot(en_iyi, label="En iyi tur")
plt.plot(ort, label="Popülasyon ortalaması")
plt.xlabel("Nesil"); plt.ylabel("Tur uzunluğu (km)")
plt.title(f"Genetik algoritma · seed = {OGRENCI_NO}")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout()
plt.savefig("ga_grafik.png", dpi=150)
print("Grafik kaydedildi: ga_grafik.png")
