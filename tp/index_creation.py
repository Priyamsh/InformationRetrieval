# -*- coding: utf-8 -*-
"""index_creation

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PNQhfQgyHpyDvDTfOKhByxoed8bEAB2a
"""

#pip install hashedindex

import nltk
nltk.download('punkt')
import re
import bs4 as bs
from nltk.tokenize import word_tokenize
import string
import pandas as pd
import hashedindex
import json
import sys

#from google.colab import drive
#drive.mount('/content/drive')

def ext_title(f_name):
  '''
  This function extracts the {docid:title}

  '''
  docs_title = {}
  with  open(f_name, "r") as fh:
    data  = fh.read()
    docs_raw  = { doc.group(1).strip():doc.group(2).strip() for doc in re.finditer(r'<doc id="([0-9]*)".*?title="(.*?)">',data,flags = re.M|re.S)}
    docs_title = { k: bs.BeautifulSoup(v,features="lxml").get_text() for k,v in docs_raw.items()}
    docs_title= dict((k.lower(), v.lower()) for k,v in docs_title.items()) #changing into lower case to avoid repeatetions

  return docs_title

def ext_document(f_name):
  '''
  This function extracts the document id and text for each
  document in the file for further processing.

  '''
  docs_final = {}
  with  open(f_name, "r") as fh:
    data  = fh.read()
    docs_raw  = { doc.group(1).strip():doc.group(2).strip() for doc in re.finditer(r'<doc id="([0-9]*)".*?>(.*?)</doc>',data,flags = re.M|re.S)}
    docs_final = { k: bs.BeautifulSoup(v,features="lxml").get_text() for k,v in docs_raw.items()}
    docs_final= dict((k.lower(), v.lower()) for k,v in docs_final.items()) #changing into lower case to avoid repeatetion

  return docs_final

def make_postinglist(docs):
  '''
  This function creates a posting list of the form {term:{docid:tf}}
  for all the terms in the list of documents

  '''
  inverted_index  =  hashedindex.HashedIndex()
  for (k,v) in docs.items():
    for tokens in nltk.word_tokenize(v):
      if tokens not in string.punctuation:
        inverted_index.add_term_occurrence(tokens,k)
  return inverted_index



def get_pldict(documents):
  '''
  This function will give posting list dictionary of the form {docid:{term:tf}
  for all documents

  '''

  pldict = hashedindex.HashedIndex()
  for (k,v) in documents.items():
    for tokens in nltk.word_tokenize(v):
      if tokens not in string.punctuation:
        pldict.add_term_occurrence(k,tokens)


  return pldict



def ext_title_from(docs):
  '''
  This function creates a posting list of the form :{docid:{term:tf}}
  for all the terms in the titles of all documents

  '''
  index  =  hashedindex.HashedIndex()
  for (k,v) in docs.items():
    for tokens in nltk.word_tokenize(v):
      if tokens not in string.punctuation:
        index.add_term_occurrence(k,tokens)
        index[k][tokens] = 10*index[k][tokens] #tittleterms have been assigned 10*termfrequency weightage to give them more importance
  return index

def ext_tittle_index(docs):
  '''
  this function will return original postinglist of title terms
  in the form {docid : {term : tf}} for all docs
  '''
  index  =  hashedindex.HashedIndex()
  for (k,v) in docs.items():
    index.add_term_occurrence(k,v)
  return index

def save_file(filename, index):
  with open(filename, "w+") as f:
    temp  = { str(k):str(json.dumps(index[k])) for k in index.items()}
    j  = json.dumps(temp)
    f.write(j)
    f.close()

def openfile(f):
  with open(f, "r+") as f:
    index=json.load(f)
    for word,string in index.items():
        index[word]=json.loads(index[word])
    return index

def main(filename):
    
    print(1)
    infile=filename
    #infile = sys.argv[1]

    documents = ext_document(infile) #we chose wiki00 file under AO folder
    posting_list = make_postinglist(documents)
    posting_list_dict = get_pldict(documents)

    title = ext_title(infile)
    title_pl = ext_title_from(title)
    title_index = ext_tittle_index(title)


    save_file("indwot.json",posting_list_dict)
    save_file("polwot.json",posting_list)
    save_file("title_pl.json",title_pl)
    save_file("title.json",title_index)

    title_pl_upt = openfile("title_pl.json")

    for (k,v) in title_pl_upt.items():
        for (a,b) in v.items():
            try:
               posting_list[a][k] = posting_list[a][k] +v[a] #we are updating the termfrequency of title terms to give them more weightage
            except:
                pass

    for (k,v) in title_pl_upt.items():
        for (a,b) in v.items():
             try:
                posting_list_dict[k][a] = posting_list_dict[k][a] + v[a] #we are updating the termfrequency of title terms to give them more weightage

             except:
                 pass

    save_file("indt.json",posting_list_dict)
    save_file("polt.json",posting_list)
    print(2)

main('wiki_00')