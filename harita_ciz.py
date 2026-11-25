from teslimat import *
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
N=noktalari_oku('noktalar.csv'); H=yollari_oku('yollar.csv')
D="Depo_Makrolog"; A=["DevletHastanesi","YasamVadisi","YuzuncuYilParki","ZeytinCafe","DogaRestaurant","BogaSteakhouse","KahveTutkusu","MissBurger"]
P="#B0245F"; DEPO="#F06292"; ARA="#6B4A57"; YOL="#EBCAD6"
et={"Depo_Makrolog":"DEPO\nMakrolog","DevletHastanesi":"Devlet Hastanesi","YasamVadisi":"Yaşam\nVadisi","YuzuncuYilParki":"100. Yıl Parkı","ZeytinCafe":"Zeytin Cafe","DogaRestaurant":"Doğa\nRestaurant","BogaSteakhouse":"Boğa\nSteakhouse","KahveTutkusu":"Kahve\nTutkusu","MissBurger":"Miss Burger"}
ara=["FileMarket","AliPasaCamii","KarakusDoner","SutlacDiyari","BuyuksaatKavurmacisi","DivanKebap"]
# döndürülmüş: kuzey sağda, doğu aşağıda
xy=lambda n:(N[n][0], -N[n][1]*0.753)
off={"Depo_Makrolog":(0,-0.0016),"DevletHastanesi":(0.0000,0.0011),"YasamVadisi":(0.0003,-0.0016),"YuzuncuYilParki":(0.0002,0.0009),"ZeytinCafe":(-0.0030,0.0007),"DogaRestaurant":(0.0002,-0.0017),"BogaSteakhouse":(0,0.0013),"KahveTutkusu":(0.0002,-0.0017),"MissBurger":(-0.0012,0.0010)}
def ciz(dosya,vurgu=None,sira=None):
    fig,ax=plt.subplots(figsize=(11,7.2))
    for a,l in H.items():
        for b,km in l:
            if a<b:
                (x1,y1),(x2,y2)=xy(a),xy(b); ax.plot([x1,x2],[y1,y2],color=YOL,lw=3,zorder=1)
    if vurgu:
        for i in range(len(vurgu)-1):
            ax.annotate("",xy=xy(vurgu[i+1]),xytext=xy(vurgu[i]),arrowprops=dict(arrowstyle="-|>",color=P,lw=3.2,mutation_scale=20,shrinkA=6,shrinkB=6),zorder=2)
    for n in N:
        x,y=xy(n)
        if n in ara:
            ax.scatter(x,y,s=60,c=ARA,zorder=3,edgecolors="white")
            continue
        c=DEPO if n==D else P; s=420 if n==D else 220
        if sira and n in sira:
            s=520
        ax.scatter(x,y,s=s,c=c,zorder=3,edgecolors="white",linewidths=2)
        if sira and n in sira:
            ax.text(x,y,str(sira[n]),color="white",fontsize=13,fontweight="bold",ha="center",va="center",zorder=5)
        dx,dy=off[n]; ax.text(x+dx,y+dy,et[n],fontsize=15,fontweight="bold",color="#3A1F2B",ha="center",va="center",zorder=4,linespacing=1.0)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    xs=[xy(n)[0] for n in N]; ys=[xy(n)[1] for n in N]
    ax.set_xlim(min(xs)-0.0012,max(xs)+0.0012); ax.set_ylim(min(ys)-0.0022,max(ys)+0.0014)
    plt.savefig("yatay_"+dosya,dpi=170,bbox_inches="tight",pad_inches=0.08); plt.close()
ciz("harita.png")
d=mesafe_tablosu(H,[D]+A,h_fonk=lambda h: kus_ucusu_h(N,h)); tur,km=kaba_kuvvet(D,A,d)
yol=[D]
for i in range(len(tur)-1): yol+=a_yildiz(H,tur[i],tur[i+1],kus_ucusu_h(N,tur[i+1]))[0][1:]
ciz("tur_harita.png",vurgu=yol,sira={n:i+1 for i,n in enumerate(tur[1:-1])})
ciz("astar_harita.png",vurgu=a_yildiz(H,D,"ZeytinCafe",kus_ucusu_h(N,"ZeytinCafe"))[0])
