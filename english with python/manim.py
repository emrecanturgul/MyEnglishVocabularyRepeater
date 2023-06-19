import random
import pandas as pd
import time
import pyttsx3
import matplotlib.pyplot as plt


kelime_dosyasi = "C:\\Users\\turgu\\Yazılım\\uniq_tr_en_dict.csv"
veri = pd.read_csv(kelime_dosyasi, on_bad_lines="skip")
i = 1
puan = 0
time_limit = 60


def metni_okut(metin):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(metin)
    engine.runAndWait()


deyim_kontrol = input(" sadece deyim çalışmak istiyor musunuz?(e/h)")
if deyim_kontrol == "h":
    while i < 10:
        start_time = time.time()
        rastgele_kelime = veri["english"].sample().values[0]
        print("{}.soru {}".format(i, rastgele_kelime))

        cevap = input("")
        if cevap == veri.loc[veri["english"] == rastgele_kelime, "turkish"].values[0]:
            print("doğru cevap")
            i += 1
            okunus = input("okunuşunu duymak istiyor musunuz(e/h)")
            if okunus == "e":
                metni_okut(rastgele_kelime)
            else:
                continue

            puan += 1
        else:
            dogru_cevap = veri.loc[
                veri["english"] == rastgele_kelime, "turkish"
            ].values[0]
            gecen_sure = int(time.time()) - int(start_time)

            print("yanlış / doğrusu=", dogru_cevap)
            okunus = input("okunuşunu duymak istiyor musunuz(e/h)")
            i += 1
            if okunus == "e":
                metni_okut(rastgele_kelime)
            else:
                continue

        gecen_sure = int(time.time()) - int(start_time)
        if gecen_sure > time_limit:
            print("süre doldu cevap vermek için daha fazla süren yok")
            break
else:
    while i < 10:
        start_time = time.time()
        deyimler = veri[veri["category"] == "idioms"]
        rastgele_deyim = deyimler.sample(1)["english"].values[0]
        print("{} kelimesinin türkçesini yazınız".format(rastgele_deyim))
        deyim_cevap = input("")
        if (
            deyim_cevap
            == veri.loc[veri["english"] == rastgele_deyim, "turkish"].values[0]
        ):
            print("doğru cevap")
            puan += 1

        else:
            dogru_deyim = veri.loc[veri["english"] == rastgele_deyim, "turkish"].values[
                0
            ]
            print("yanlış cevap. Doğru cevap:", dogru_deyim)
        i += 1
        gecen_sure = time.time() - start_time
        if gecen_sure > time_limit:
            print("süre doldu cevap vermek için daha fazla süren yok")
            break

print(puan)
dosya_adi = "istatistikler.txt"


def istatistikleri_kaydetme(puan):
    with open(dosya_adi, "a") as dosya:
        dosya.write("toplam puan {}\n".format(puan))
    print("istatistikler başarıyla kaydedildi")


istatistikleri_kaydetme(puan)

puanlar = []
with open("istatistikler.txt", "r") as dosya:
    satir = dosya.readlines()
    for line in satir:
        if "toplam puan" in line:
            puanlar.append(int(line.split()[-1]))

print("puanlar", puanlar)


def grafik_ciz(puanlar):
    x = range(1, len(puanlar) + 1)
    y = puanlar

    plt.plot(x, y, marker="o")
    plt.xlabel("Deneme Numarası")
    plt.ylabel("Puan")
    plt.title("Puan İstatistikleri")
    plt.grid(True)
    plt.show()


grafik_ciz(puanlar)
