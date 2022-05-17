import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("persona.csv")
df.head() # Veriye gözlem yapmak için ilk kullanmamız gereken head ve tail'dir.

df.shape # Satır - Sutün sayısını öğrenmek için kullanıyoruz. (5000, 5)

df.info() # veri setimiz hakkında bilgi edinmek için kullanıyoruz.

df.describe().T # sayısal değişkenlerimiz hakkında kısaca bir istatistiksel özet almak için kullanıyoruz.

# Hangi fiyattan kaçar adet satış gerçekleştiğine bakalım.
df["PRICE"].nunique()
df["PRICE"].value_counts()

# Hangi ülkeden kaçar tane satış olduğuna göz atalım.
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

# Ülkelere göre satışlardan toplam ne kadar kazanılmış olduğuna göz atalım. İki farklı yoldan biri tercih edilebilir.
#df.groupby("COUNTRY")['PRICE'].sum()
df.groupby("COUNTRY").agg({"PRICE" : 'sum'})

# Ülkelere göre PRICE ortalamalarına göz atalım. İki farklı yoldan biri tercih edilebilir.
#df.groupby("COUNTRY")['PRICE'].mean()
df.groupby("COUNTRY").agg({'PRICE' : 'mean'})

# SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({'PRICE' : 'mean'})

# COUNTRY-SOURCE kırılımında PRICE ortalamalarına göz atalım.
df.groupby(["COUNTRY", "SOURCE"]).agg({'PRICE' : 'mean'})

# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlarına göz atalım.
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({'PRICE' : 'mean'})

# PRICE'a göre sıralama yapıp başka bir dataframe'e atalım.
agg_df = df.groupby(by=["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)

# Groupby sonrası gelen Indeksi değişken yapalım.
agg_df = agg_df.reset_index()

#Age sayısal değişkenini kategorik değişkene çeviremeye çalışalım.
bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim.
my_labels = ['0_18', '19_23', '24-30', '31-40', '41_' + str(agg_df["AGE"].max())]
agg_df['age_cat'] = pd.cut(agg_df['AGE'], bins, labels=my_labels)

# Yeni seviye tabanlı müşterileri (persona) tanımlamaya çalışalım.
# Gözlem değerlerine nasıl erişiriz?
for row in agg_df.values:
    print(row)
agg_df['customers_level_based'] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Sadece kullanacağımız değişkenleri alalım.
agg_df = agg_df[["customers_level_based", "PRICE"]]

# Oluşturduğumuz segmentlerden tekrarlayan var mı kontrol edip, PRICE'a göre ortalamalarını alalım.
agg_df["customers_level_based"].value_counts()
agg_df = agg_df.groupby('customers_level_based').agg({'PRICE': "mean"})

#customers_level_based indexini değişken olarak getirelim.
agg_df = agg_df.reset_index()

# Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"PRICE" : ["mean", "max", "sum"]})


# Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
new_user = 'TUR_ANDROID_FEMALE_24-30'
agg_df[agg_df["customers_level_based"] == new_user]