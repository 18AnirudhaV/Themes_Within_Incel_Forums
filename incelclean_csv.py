import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.metrics import pairwise_distances
from numpy import array
from scipy.linalg import svd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from random import seed
from random import randint
import nltk
import string
seed(1)
#raw_txt = pd.read_csv("Incels_co_FULL.csv",sep='\t', lineterminator='\r',encoding='utf-8', parse_dates=True, dtype={"txtBody":"string","txtBody_Clean":"string","txtPostDate":"string"})
raw_txt = pd.read_csv("Incels_co_FULL.csv",sep='\t', lineterminator='\r',encoding='utf-8', parse_dates=True, usecols=['dtPostDate'], nrows=500000 ,dtype={"txtBody":"string","txtBody_Clean":"string","txtPostDate":"string", "dtPostDate":"string"}, verbose=True)

#file2 = open("Incels_clean_final.txt","w",encoding="utf-8")
file2 = open("Incels_dates.txt","w",encoding="utf-8")
for line in raw_txt["dtPostDate"]:
    space = line.find(" ")
    new_line = line[0:space]
    file2.write(new_line + "\n")

def process_text(text):
    soup = BeautifulSoup(text, "html.parser")
    for elm in soup.find_all():
        elm.decompose()
    cleantext = str(soup)
    #cleantext = re.sub(CLEANR, '', raw_html)
    cleantext_nl = re.sub(r'http\S+', '', cleantext)
    #cleantext_f = re.sub('[^a-zA-Z0-9 \n\.]', '', cleantext_nl)
    cleantext_f = re.sub(r'\d+', '', cleantext_nl)
    cleantext_f1 = re.sub('[,\.!?]', '', cleantext_f)
    new_str = cleantext_f1.replace("Â", "")
    new_str = new_str.replace("[hr]", "")
    new_str = new_str.replace("[font=helvetica arial sans-serif]", "")
    new_str = new_str.replace("[/font]", "")
    new_str = new_str.replace("&gt;", "")
    new_str = new_str.replace("[video=youtube]", "")
    return new_str
raw_txt["clean_text"] = raw_txt["txtBody"].apply(process_text)
print(raw_txt["clean_text"])
c = 0
for line in raw_txt["txtBody_Clean"]:
    #Removes leftover HTML tags
    f_strt = 0
    s_strt = 0
    v_strt = 0
    q_strt = 0
    c = c + 1
    if (c % 10000 == 0):
        print(c)
    new_str = str(line)
    a = 0
    while("Click to expand..." in new_str):
        a = a + 1
        if (a > 100):
            print(new_str)
            print("Click")
            break
        pst_strt = new_str.find("...")
        new_str = new_str[pst_strt + 3:-1].lstrip()
    a = 0
    #Removes original post text from replies 
    while ("RE: " in new_str):
        a = a + 1
        if (a > 100):
            print(new_str)
            print("RE")
            break
        pst_strt = new_str.find("RE: ")
        pst_end = new_str.find("    ")
        pst = new_str[pst_strt:pst_end]
        new_str = new_str.replace(pst,"")
    a = 0
    while (f_strt != -1 or s_strt != -1 or v_strt != -1 or q_strt != -1):
        a = a + 1
        if (a > 100):
            print("F S Q V")
            print(new_str)
            break
        f_strt = new_str.find("[font=")
        s_strt = new_str.find("[size=")
        v_strt = new_str.find("[video=")
        q_strt = new_str.find("[quote")
        if (f_strt == -1 and s_strt == -1 and v_strt == -1 and q_strt == -1):
            break
        tmp = new_str[f_strt:-1]
        tmp2 = new_str[s_strt:-1]
        tmp3 = new_str[v_strt:-1]
        tmp4 = new_str[q_strt:-1]
        f_end = tmp.find("]")
        if f_end == -1:
            f_end = 5
        s_end = tmp2.find("]")
        if s_end == -1:
            s_end = 5
        v_end = tmp3.find("]")
        if v_end == -1:
            v_end = 6
        q_end = tmp4.find("]")
        if q_end == -1:
            q_end = 6
        font = new_str[f_strt:f_end + f_strt + 1]
        s = new_str[s_strt:s_end + s_strt + 1]
        v = new_str[v_strt:v_end + v_strt + 1]
        q = new_str[q_strt:q_end + q_strt + 1]
        new_str = new_str.replace(font, "")
        new_str = new_str.replace(s, "")
        new_str = new_str.replace(v, "")
        new_str = new_str.replace(q, "")
    cleantext_nl = re.sub(r'http\S+', '', new_str)
    cleantext_f = re.sub(r'\d+', '', cleantext_nl)
    new_str = re.sub('[,\.!?]', '', cleantext_f)
    new_str = new_str.replace("Â","")
    new_str = new_str.replace("[hr]", "")
    new_str = new_str.replace("[/size]", "")
    new_str = new_str.replace("[attachment=]", "")
    new_str = new_str.replace("[img=x]", "")
    new_str = new_str.replace("[/font]", "")
    new_str = new_str.replace("youtube]", "")
    new_str = new_str.replace("&gt;", "")
    new_str = new_str.replace("<NA>", "")
    new_str = new_str.replace("[/quote]", "")
    new_str = new_str.replace("Click to expand", "")
    file2.write(new_str+"\n")
file2.close()