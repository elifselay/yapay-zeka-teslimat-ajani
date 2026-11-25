# Kendi Haritanda Teslimat Ajanı: Çatalca Merkez

Yapay Zeka dersi dönem projesi · Elif Selay Yener · 2322120080
İstanbul Esenyurt Üniversitesi · Bilgisayar Mühendisliği · 2026–2027 Güz

Çatalca merkezde bir depodan (Makrolog) çıkan kurye 8 adrese paket götürür.

- **A\*** ile depodan her adrese en kısa yol bulunur (sezgisel fonksiyon: kuş uçuşu mesafe).
- **Genetik algoritma** ile 8 adresi gezip depoya dönen en kısa tur bulunur.
- **Ek puan:** 8! = 40.320 sıralama kaba kuvvetle denenip genetik algoritmanın sonucu doğrulanır.

## Dosyalar

| Dosya | Ne işe yarar |
|---|---|
| `teslimat.py` | A\*, genetik algoritma ve kaba kuvvet fonksiyonları |
| `calistir.py` | Bütün sonuçları ekrana yazar, `ga_grafik.png` grafiğini çizer |
| `harita_ciz.py` | Harita, A\* yolu ve tur haritalarını çizer |
| `noktalar.csv` | 15 nokta: ad, enlem, boylam (Google Haritalar) |
| `yollar.csv` | 24 yol: iki nokta ve km (Google Haritalar araç rotası) |
| `ornek_yollar.csv` | Ödev belgesindeki Örnekşehir haritası (test için) |
| `sonuclar/` | Rapordaki haritalar ve grafik |
| `Rapor_...pdf`, `Sunum_...pdf` | Rapor ve sunum |

## Çalıştırma

Python 3 gerekir.

```
pip install -r requirements.txt
python calistir.py
python harita_ciz.py
```

## Sonuçlar

- Örnekşehir testi: S-A-G-F-B-S belgedeki sonuçla aynı çıkar.
- A\*: kuş uçuşu sezgisiyle 71 düğüm açıldı, h = 0 (UCS) ile 77.
- En kısa tur **11,99 km**: Depo → Devlet Hastanesi → Yaşam Vadisi → Doğa Restaurant → 100. Yıl Parkı → Zeytin Cafe → Miss Burger → Boğa Steakhouse → Kahve Tutkusu → Depo
- Genetik algoritma (seed 2322120080…2322120089) 10 çalıştırmanın 10'unda bu optimumu buldu; kaba kuvvet de aynı sonucu verdi.
