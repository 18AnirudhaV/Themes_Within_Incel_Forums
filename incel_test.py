import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

path = "Incels_co_FULL.txt_Part0.txt"
fo = open(path, "r+")
fo.readline()
psts = []
for i in range(10):
    str = fo.readline()
    info_start = 48
    info_str = str[info_start:-1].lstrip()
    pst_start = info_str.find("PM")+2
    pst_str = info_str[pst_start:-1].lstrip()
    pst_end = pst_str.find("		")
    new_str = pst_str[0:pst_end]
    new_str = new_str.replace("<br>","")
    new_str = new_str.replace("Â","")
    psts.append(new_str)
    print("FINISHED STR:"+new_str)
fo.close()

CountVec = CountVectorizer(ngram_range=(1, 1),
                           stop_words='english')

Count_data = CountVec.fit_transform(psts)

cv_dataframe = pd.DataFrame(Count_data.toarray(), columns=CountVec.get_feature_names())
print(cv_dataframe)
