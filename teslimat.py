import csv, heapq, math, random, itertools

# ---------- Veri ----------
def yollari_oku(dosya):
    harita = {}
    with open(dosya, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            a, b, km = r["a"].strip(), r["b"].strip(), float(r["km"])
            harita.setdefault(a, []).append((b, km))
            harita.setdefault(b, []).append((a, km))   # yollar çift yönlü
    return harita

def noktalari_oku(dosya):
    with open(dosya, encoding="utf-8") as f:
        return {r["ad"].strip(): (float(r["enlem"]), float(r["boylam"])) for r in csv.DictReader(f)}

def haversine(p, q):
    """İki koordinat arasındaki kuş uçuşu mesafe (km)."""
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (*p, *q))
    a = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def kus_ucusu_h(noktalar, hedef):
    return {ad: haversine(k, noktalar[hedef]) for ad, k in noktalar.items()}

# ---------- A* ----------
def a_yildiz(harita, bas, hedef, h=None):
    """f = g + h. Hedef testi düğüm AÇILIRKEN yapılır, eşitlikte alfabetik sıra.
    h=None verilirse h = 0 olur (düşük maliyetli arama)."""
    if h is None:
        h = {}
    sinir = [(h.get(bas, 0), bas, 0, [bas])]          # (f, şehir, g, rota)
    acilanlar, acilma_sirasi = set(), []
    while sinir:
        f, sehir, g, rota = heapq.heappop(sinir)       # en küçük f, eşitse alfabetik
        if sehir in acilanlar:
            continue
        acilanlar.add(sehir)
        acilma_sirasi.append(sehir)
        if sehir == hedef:                              # açılırken hedef testi
            return rota, g, acilma_sirasi
        for komsu, km in harita[sehir]:
            if komsu not in acilanlar:
                yeni_g = g + km
                heapq.heappush(sinir, (yeni_g + h.get(komsu, 0), komsu, yeni_g, rota + [komsu]))
    return None, math.inf, acilma_sirasi

def mesafe_tablosu(harita, noktalar_listesi, h_fonk=None):
    """Depo + adresler arasındaki bütün çiftlerin A* mesafesi."""
    d = {}
    for a, b in itertools.combinations(noktalar_listesi, 2):
        h = h_fonk(b) if h_fonk else None
        _, km, _ = a_yildiz(harita, a, b, h)
        d[(a, b)] = d[(b, a)] = km
    return d

# ---------- Genetik algoritma ----------
def tur_uzunlugu(birey, depo, d):
    rota = [depo] + list(birey) + [depo]
    return sum(d[(rota[i], rota[i + 1])] for i in range(len(rota) - 1))

def rulet_sec(pop, uygunluk, rng):
    toplam = sum(uygunluk)
    r, birikim = rng.random() * toplam, 0.0
    for birey, f in zip(pop, uygunluk):
        birikim += f
        if birikim >= r:
            return birey
    return pop[-1]

def sirali_caprazlama(p1, p2, rng):
    """Sıralı çaprazlama (OX): p1'den bir dilim al, kalan genleri p2'deki sırayla doldur."""
    n = len(p1)
    i, j = sorted(rng.sample(range(n), 2))
    cocuk = [None] * n
    cocuk[i:j + 1] = p1[i:j + 1]
    kalan = [g for g in p2 if g not in cocuk]
    for k in range(n):
        if cocuk[k] is None:
            cocuk[k] = kalan.pop(0)
    return cocuk

def yer_degistir(birey, rng):
    b = list(birey)
    i, j = rng.sample(range(len(b)), 2)
    b[i], b[j] = b[j], b[i]
    return b

def genetik_algoritma(depo, adresler, d, pop_boyu=50, nesil=200, pc=0.9, pm=0.1, seed=0):
    rng = random.Random(seed)
    pop = [rng.sample(adresler, len(adresler)) for _ in range(pop_boyu)]
    en_iyi_gecmis, ort_gecmis = [], []
    for _ in range(nesil):
        uzunluklar = [tur_uzunlugu(b, depo, d) for b in pop]
        uygunluk = [1 / u for u in uzunluklar]          # f = 1 / tur uzunluğu
        en_iyi = pop[uzunluklar.index(min(uzunluklar))]
        en_iyi_gecmis.append(min(uzunluklar))
        ort_gecmis.append(sum(uzunluklar) / len(uzunluklar))
        yeni = [list(en_iyi)]                             # elitizm
        while len(yeni) < pop_boyu:
            p1, p2 = rulet_sec(pop, uygunluk, rng), rulet_sec(pop, uygunluk, rng)
            cocuk = sirali_caprazlama(p1, p2, rng) if rng.random() < pc else list(p1)
            if rng.random() < pm:
                cocuk = yer_degistir(cocuk, rng)
            yeni.append(cocuk)
        pop = yeni
    uzunluklar = [tur_uzunlugu(b, depo, d) for b in pop]
    en_iyi = pop[uzunluklar.index(min(uzunluklar))]
    return [depo] + en_iyi + [depo], min(uzunluklar), en_iyi_gecmis, ort_gecmis

def kaba_kuvvet(depo, adresler, d):
    """Ek puan: bütün sıralamaları dener."""
    en_iyi = min(itertools.permutations(adresler), key=lambda p: tur_uzunlugu(p, depo, d))
    return [depo] + list(en_iyi) + [depo], tur_uzunlugu(en_iyi, depo, d)
