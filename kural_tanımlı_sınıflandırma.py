##############################################################################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
###############################################################################################

##############################################################################################
# İş Problemi
###############################################################################################

##############################################################################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak
# seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler
# oluşturup bu segmentlere göre yeni gelebilecek müşterilerin
# şirkete ortalama ne kadar kazandırabileceğini tahmin etmek
# istemektedir.
###############################################################################################

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.

##############################################################################################
# Veri Seti Hikayesi
###############################################################################################

#Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu
#ürünleri satın alan kullanıcıların bazı demografik bilgilerini barındırmaktadır. Veri
#seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı
#tablo tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir
#kullanıcı birden fazla alışveriş yapmış olabilir.

##############################################################################################
# GÖREV 1
###############################################################################################

##############################################################################################
# Soru 1 : persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
###############################################################################################

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
df = pd.read_csv("persona.csv")
df.shape
df.info()

##############################################################################################
# Soru 2 : Kaç unique SOURCE vardır? Frekansları nedir?
###############################################################################################

df['SOURCE'].nunique()
df['SOURCE'].value_counts()

##############################################################################################
# Soru 3 : Kaç unique PRICE vardır?
###############################################################################################

df['PRICE'].nunique()

##############################################################################################
# Soru 4 : Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
###############################################################################################

df['PRICE'].value_counts()

##############################################################################################
# Soru 5 : Hangi ülkeden kaçar tane satış olmuş?
###############################################################################################

df['COUNTRY'].value_counts()
df.groupby("COUNTRY")['PRICE'].count()

##############################################################################################
# Soru 6 : Ülkelere göre satışlardan toplam ne kadar kazanılmış?
###############################################################################################

df.groupby("COUNTRY")['PRICE'].sum()

df.groupby("COUNTRY").agg({"PRICE" : 'sum'})

##############################################################################################
# Soru 7 : SOURCE türlerine göre satış sayıları nedir?
###############################################################################################

df['SOURCE'].value_counts()

##############################################################################################
# Soru 8 : Ülkelere göre PRICE ortalamaları nedir?
###############################################################################################

df.groupby("COUNTRY")['PRICE'].mean()

df.groupby("COUNTRY").agg({'PRICE' : 'mean'})

##############################################################################################
# Soru 9 : SOURCE'lara göre PRICE ortalamaları nedir?
###############################################################################################

df.groupby("SOURCE").agg({'PRICE' : 'mean'})

##############################################################################################
# Soru 10 : COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
###############################################################################################

df.groupby(["COUNTRY", "SOURCE"]).agg({'PRICE' : 'mean'})

##############################################################################################
# GÖREV 2 : COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
###############################################################################################

df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({'PRICE' : 'mean'})

##############################################################################################
# GÖREV 3 : Çıktıyı PRICE’a göre sıralayınız.
###############################################################################################

#Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
#Çıktıyı agg_df olarak kaydediniz.

#df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({'PRICE' : 'mean'}).sort_values("PRICE", ascending=False)

agg_df = df.groupby(by=["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()

##############################################################################################
# GÖREV 4 : Indekste yer alan isimleri değişken ismine çeviriniz.
###############################################################################################

agg_df = agg_df.reset_index()
agg_df.head()

##############################################################################################
# GÖREV 5 : Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
###############################################################################################

#Age sayısal değişkenini kategorik değişkene çeviriniz.
#Aralıkları ikna edici şekilde oluşturunuz.
#Örneğin: ‘0_18', ‘19_23', '24_30', '31_40', '41_70'

bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim.
my_labels = ['0_18', '19_23', '24-30', '31-40', '41_' + str(agg_df["AGE"].max())]

#age'i bölelim:
agg_df['age_cat'] = pd.cut(agg_df['AGE'], bins, labels=my_labels)
agg_df.head()

##############################################################################################
# GÖREV 6 : Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
###############################################################################################

#Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
#Yeni eklenecek değişkenin adı: customers_level_based
#Önceki soruda elde edeceğiniz çıktıdaki gözlemleri bir araya getirerek customers_level_based değişkenini oluşturmanız gerekmektedir.

#Dikkat! List comprehension ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
#Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18. Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

#Değişken isimleri
agg_df.columns

#Gözlem değerlerine nasıl erişiriz?
for row in agg_df.values:
    print(row)

#Değişkenleri alt tire ile birleştirmek için list comprehension yapısı kullanmalıyız.
agg_df['customers_level_based'] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

#Bizden istenmeyen değişkenleri çıkaralım
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()

# Tekrarlayan var mı kontrol edelim
agg_df["customers_level_based"].value_counts()

# Segmentler Price ortalaması alarak tekilleştirilmeli
agg_df = agg_df.groupby('customers_level_based').agg({'PRICE': "mean"})
agg_df.head()

#customers_level_based değişken olmaktan kurtaralım
agg_df = agg_df.reset_index()
agg_df.head()

#Segmentlerin tekil olduğunu kontrol edelim
agg_df["customers_level_based"].value_counts()

##############################################################################################
# GÖREV 7 : Yeni müşterileri (personaları) segmentlere ayırınız.
###############################################################################################

#Yeni müşterileri (Örnek: USA_ANDROID_MALE_0_18) PRICE’a göre 4 segmente ayırınız.
#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz.
#Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE" : ["mean", "max", "sum"]})

##############################################################################################
# GÖREV 8 : Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
###############################################################################################

#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

agg_df.tail(50)
new_user = 'TUR_ANDROID_FEMALE_31-40'

agg_df[agg_df["customers_level_based"] == new_user]

#35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = 'FRA_IOS_FEMALE_31-40'

agg_df[agg_df["customers_level_based"] == new_user]