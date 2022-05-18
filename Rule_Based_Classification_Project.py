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
my_labels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]
agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins, labels=my_labels)

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
new_user = 'BRA_ANDROID_FEMALE_24_30'
agg_df[agg_df["customers_level_based"] == new_user]

# Bonus : Kullanıcıdan değer alarak potalsiyel müşteri segmentini ve getirisini hesaplayalım.
print('*********** Kural Bazlı Potalsiyel Müşteri Getirisi Hesaplama ************')
while True:
  print()
  print("Ülkeler : \n\n1.{0}\n2.{1}\n3.{2}\n4.{3}\n5.{4}\n".format((df['COUNTRY'].unique()[0].upper()), (df['COUNTRY'].unique()[1].upper()), (df['COUNTRY'].unique()[2].upper()), (df['COUNTRY'].unique()[3].upper()), (df['COUNTRY'].unique()[4].upper()), (df['COUNTRY'].unique()[5].upper())))
  country = str(input("İstediğiniz ülkeyi yazınız ->\n "))
  print("İşletim sistemleri : \n\n1.{0}\n2.{1}\n".format((df['SOURCE'].unique()[0].upper()), (df['SOURCE'].unique()[1].upper())))
  source = str(input("İstediğiniz işletim sistemini yazınız -> \n"))
  print("Cinsiyetler : \n\n1.{0}\n2.{1}\n".format((df['SEX'].unique()[0].upper()), (df['SEX'].unique()[1].upper())))
  sex = str(input("İstediğiniz cinsiyeti yazınız -> \n"))
  age = int(input("Yaşı giriniz  -> \n"))
  if age < int(my_labels[0][2:]):
      age = my_labels[0]
    elif (age >= int(my_labels[0][2:])) & (age < int(my_labels[1][3:])):
      age = my_labels[1]
    elif (age >= int(my_labels[1][3:])) & (age < int(my_labels[2][3:])):
        age = my_labels[2]
    elif (age >= int(my_labels[2][3:])) & (age < int(my_labels[3][3:])):
        age = my_labels[3]
    else:
        age = my_labels[4]
  persona = (country.upper() + "_" + source.upper() + "_" + sex.upper() + "_" + age)
  print(persona)
  new_customer = agg_df[agg_df['customers_level_based'] == persona]
  print(f"Segmenti : {str(new_customer.iloc[0]['SEGMENT'])}")
  print(f"Potansiyel getirisi : {str(new_customer.iloc[0]['PRICE'])}")
  break
  
# Bonus : Fonksiyon ile potansiyel getiriyi hesaplayalım.
def calc_segment(dataframe, Country, Source, Sex, Age):
    if Age < int(my_labels[0][2:]):
        Age = my_labels[0]
    elif (Age >= int(my_labels[0][2:])) & (Age < int(my_labels[1][3:])):
        Age = my_labels[1]
    elif (Age >= int(my_labels[1][3:])) & (Age < int(my_labels[2][3:])):
        Age = my_labels[2]
    elif (Age >= int(my_labels[2][3:])) & (Age < int(my_labels[3][3:])):
        Age = my_labels[3]
    else:
        Age = my_labels[4]
    Persona = (Country.upper() + "_" + Source.upper() + "_" + Sex.upper() + "_" + Age)
    print(Persona)
    New_Customer = agg_df[agg_df['customers_level_based'] == Persona]
    print(f"Segmenti : {str(New_Customer.iloc[0]['SEGMENT'])}")
    print(f"Potansiyel getirisi : {str(New_Customer.iloc[0]['PRICE'])}")

calc_segment(agg_df, 'TUR', 'IOS', 'Male', 15)
