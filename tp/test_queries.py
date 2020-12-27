#!/usr/bin/env python
# coding: utf-8

# In[163]:


def take_query_input():
    query = input("Enter you query : ")
    return query.lower()


# In[209]:


import json
import pandas as pd

def openindex_choice(choice):
    if(choice==1):
        f=open('indt.json')
        index=json.load(f)
    else:
        f=open('indwot.json')
        index=json.load(f)
    for word,string in index.items():
        index[word]=json.loads(index[word])
    return index


# In[210]:


def openpostinglist_choice(choice):
    if(choice==1):
        q=open('polt.json')
        postinglist=json.load(q)
    else:
        q=open('polwot.json')
        postinglist=json.load(q)
    for docid,string in postinglist.items():
        postinglist[docid]=json.loads(postinglist[docid])
    return postinglist,len(postinglist.keys())


# In[211]:


def openindex():
    f=open('ind.json')
    index=json.load(f)
    for word,string in index.items():
        index[word]=json.loads(index[word])
    return index


# In[212]:


def openpostinglist():
    q=open('pol.json')
    postinglist=json.load(q)
    for docid,string in postinglist.items():
        postinglist[docid]=json.loads(postinglist[docid])
    return postinglist,len(postinglist.keys())


# In[166]:


def opentitle():
    q=open('title.json')
    title=json.load(q)
    for docid,string in title.items():
        title[docid]=list(json.loads(string).keys())[0].title()
    return title


# In[167]:


from spellchecker import SpellChecker

def correctquery(query):
    spell=SpellChecker()
    spell.distance=1
    words=query.split(" ")
    corrected=[]
    for word in words:
        corrected.append(spell.correction(word))
    return " ".join(corrected)


# In[168]:


def build_champion_list(r,index):
    champion_list={}
    for word,word_index in index.items():
        word_index_temp={k: v for k, v in sorted(word_index.items(), key=lambda item: item[1],reverse=True)}
        count=r
        champion_list[word]=[]
        for docid in word_index_temp.keys():
            if(count==0):
                break
            else:
                champion_list[word].append(docid)
                count=count-1
    return champion_list


# In[169]:


import math

def form_query_vector(query,idf_values):
    query_tf={}
    for w in query.strip().split(" "):
        if(w in query_tf.keys()):
            freq=query_tf[w];
            query_tf[w]=freq+1;
        else:
            query_tf[w]=1;
    query_vector={}
    for key,value in query_tf.items():
        if(key in idf_values.keys()):
            query_vector[key]=(1+math.log(value,10))*(idf_values[key])
        else:
            query_vector[key]=(1+math.log(value,10))
    query_norm_vector={}
    values=query_vector.values();
    values=[x*x for x in values]
    for key,value in query_vector.items():
        query_norm_vector[key]=(value/math.pow(sum(values),0.5))
    return query_norm_vector


# In[170]:


def build_idf_vector(index,no_of_docs):
    idf_values={}
    for word,word_index in index.items():
        length=len(index[word].keys())
        idf_values[word]=math.log((no_of_docs/length),10)
    return idf_values


# In[171]:


def build_doc_vector_for_a_word(word,index,doc_dict):
    for docid,tf in index[word].items():
        if(docid in doc_dict.keys()):
            if(word not in doc_dict[docid].keys()):
                doc_dict[docid][word]=1+math.log(tf,10)
            else:
                pass
        else:
            doc_dict[docid]={};
            doc_dict[docid][word]=1+math.log(tf,10);


# In[172]:


def build_entire_doc_dict(query,index,posting_list):
    doc_dict={}
    for w in query.strip().split(" "):
        if(w in index.keys()):
            build_doc_vector_for_a_word(w,index,doc_dict)
        else:
            pass
    for docid in doc_dict.keys():
        doc_vector=doc_dict[docid]
        overlap=len(doc_vector.keys())
        for word,tf in doc_vector.items():
            doc_vector[word]=tf*overlap
    for docid in doc_dict.keys():
        posting_list_for_docid=posting_list[docid]
        for word,tfscore in posting_list_for_docid.items():
            if(word in doc_dict[docid].keys()):
                pass
            else:
                doc_dict[docid][word]=1+math.log(tfscore,10);
    for key,doc_vector in doc_dict.items():
        values=doc_dict[key].values()
        values=[x*x for x in values]
        div=math.pow(sum(values),0.5)
        for word,tfwt in doc_vector.items():
            tfscore=doc_vector[word]
            doc_vector[word]=tfscore/div
    
        
    return doc_dict


# In[173]:


def build_doc_vector_using_championlist(word,index,doc_dict,champion_list,posting_list):
    for docid in champion_list[word] + list(doc_dict.keys()):
        if(docid in doc_dict.keys()):
            if((word not in doc_dict[docid].keys()) and (word in posting_list[docid].keys())):
                doc_dict[docid][word]=1+math.log(index[word][docid],10)
            else:
                pass
        else:
            doc_dict[docid]={};
            doc_dict[docid][word]=1+math.log(index[word][docid],10);


# In[174]:


def complete_doc_vector_using_championlist(word,index,doc_dict,champion_list,posting_list):
    for docid in list(doc_dict.keys()):
        if(docid in doc_dict.keys()):
            if((word not in doc_dict[docid].keys()) and (word in posting_list[docid].keys())):
                doc_dict[docid][word]=1+math.log(index[word][docid],10)
            else:
                pass
        else:
            doc_dict[docid]={};
            doc_dict[docid][word]=1+math.log(index[word][docid],10);


# In[175]:


def build_entire_doc_dict_using_championlist(query,index,postinglist,champion_list):
    doc_dict={}
    for w in query.strip().split(" "):
        if(w in index.keys()):
            build_doc_vector_using_championlist(w,index,doc_dict,champion_list,postinglist)
        else:
            pass
    for w in query.strip().split(" "):
        if(w in index.keys()):
            complete_doc_vector_using_championlist(w,index,doc_dict,champion_list,postinglist)
        else:
            pass
    for docid in doc_dict.keys():
        doc_vector=doc_dict[docid]
        overlap=len(doc_vector.keys())
        for word,tf in doc_vector.items():
            doc_vector[word]=tf*overlap
    for docid in doc_dict.keys():
        posting_list_for_docid=postinglist[docid]
        for word,tfscore in posting_list_for_docid.items():
            if(word in doc_dict[docid].keys()):
                pass
            else:
                doc_dict[docid][word]=1+math.log(tfscore,10);
    for key,doc_vector in doc_dict.items():
        values=doc_dict[key].values()
        values=[x*x for x in values]
        div=math.pow(sum(values),0.5)
        for word,tfwt in doc_vector.items():
            tfscore=doc_vector[word]
            doc_vector[word]=tfscore/div
    
        
    return doc_dict


# In[176]:


def build_entire_doc_dict_using_championlist_choice(query,index,postinglist,champion_list,choice):
    doc_dict={}
    for w in query.strip().split(" "):
        if(w in index.keys()):
            build_doc_vector_using_championlist(w,index,doc_dict,champion_list,postinglist)
        else:
            pass
    for w in query.strip().split(" "):
        if(w in index.keys()):
            complete_doc_vector_using_championlist(w,index,doc_dict,champion_list,postinglist)
        else:
            pass
    if(choice==1):
        for docid in doc_dict.keys():
            doc_vector=doc_dict[docid]
            overlap=len(doc_vector.keys())
            for word,tf in doc_vector.items():
                doc_vector[word]=tf*overlap
    else:
        pass
    for docid in doc_dict.keys():
        posting_list_for_docid=postinglist[docid]
        for word,tfscore in posting_list_for_docid.items():
            if(word in doc_dict[docid].keys()):
                pass
            else:
                doc_dict[docid][word]=1+math.log(tfscore,10);
    for key,doc_vector in doc_dict.items():
        values=doc_dict[key].values()
        values=[x*x for x in values]
        div=math.pow(sum(values),0.5)
        for word,tfwt in doc_vector.items():
            tfscore=doc_vector[word]
            doc_vector[word]=tfscore/div
    
        
    return doc_dict


# In[177]:


def calculate_score_for_a_document(docid,doc_dict_for_docid,query_vector,doc_ranking):
    rank_score=0
    for word,score in query_vector.items():
        if(word in doc_dict_for_docid.keys()):
            rank_score+=(score)*(doc_dict_for_docid[word])
        else:
            pass
    doc_ranking[docid]=rank_score


# In[178]:


import time

def calculate_ranking_of_documents_using_champion_list(r,k):
    begin=time.time()
    query=take_query_input()
    query=correctquery(query)
    index=openindex()
    title=opentitle()
    posting_list,no_of_docs=openpostinglist()
    champion_list=build_champion_list(r,index)
    #print(champion_list)
    idf_values=build_idf_vector(index,no_of_docs)
    query_vector=form_query_vector(query,idf_values)
    #print(query_vector)
    #doc_dict=build_entire_doc_dict(query,index,posting_list)
    #print(doc_dict)
    doc_dict=build_entire_doc_dict_using_championlist(query,index,posting_list,champion_list)
    doc_ranking={}
    for docid,docid_vector in doc_dict.items():
        calculate_score_for_a_document(docid,docid_vector,query_vector,doc_ranking)
    doc_ranking={k: v for k, v in sorted(doc_ranking.items(), key=lambda item: item[1],reverse=True)}
    if(k>len(doc_ranking.keys())):
        k=len(doc_ranking.keys())
    first_k=list(doc_ranking.keys())[0:k]
    df=pd.DataFrame(columns=[['DOCID','Title','Score']])
    for key in first_k:
        df.loc[len(df.index)]=[key,title[key],doc_ranking[key]]
    end=time.time()
    print(end-begin)
    return df


# In[179]:


def calculate_ranking_of_documents(r,k):
    begin=time.time()
    query=take_query_input()
    query=correctquery(query)
    index=openindex()
    title=opentitle()
    posting_list,no_of_docs=openpostinglist()
    champion_list=build_champion_list(r,index)
    idf_values=build_idf_vector(index,no_of_docs)
    query_vector=form_query_vector(query,idf_values)
    #print(query_vector)
    doc_dict=build_entire_doc_dict(query,index,posting_list)
    #print(doc_dict)
    #doc_dict=build_entire_doc_dict_using_championlist(query,index,posting_list,champion_list)
    doc_ranking={}
    for docid,docid_vector in doc_dict.items():
        calculate_score_for_a_document(docid,docid_vector,query_vector,doc_ranking)
    doc_ranking={k: v for k, v in sorted(doc_ranking.items(), key=lambda item: item[1],reverse=True)}
    if(k>len(doc_ranking.keys())):
        k=len(doc_ranking.keys())
    first_k=list(doc_ranking.keys())[0:k]
    df=pd.DataFrame(columns=[['DOCID','Title','Score']])
    for key in first_k:
        df.loc[len(df.index)]=[key,title[key],doc_ranking[key]]
    end=time.time()
    print(end-begin)
    return df


# In[213]:


def calculate_all(k):
    count=input("1:Examine normal IR(with all modifications)\n2:Examine championlist modification\n3:Examine title term modification\n4:Examine query overlap modification\n")
    query=take_query_input()
    query=correctquery(query)
    if(int(count) != 3):
        index=openindex_choice(1)
        title=opentitle()
        posting_list,no_of_docs=openpostinglist_choice(1)
    else:
        index=openindex_choice(1)
        title=opentitle()
        posting_list,no_of_docs=openpostinglist_choice(1)
        index0=openindex_choice(0)
        posting_list0,no_of_docs1=openpostinglist_choice(0)
    champion_list=build_champion_list(10,index)
    idf_values=build_idf_vector(index,no_of_docs)
    query_vector=form_query_vector(query,idf_values)
    #print(query_vector)
    begin=time.time()
    if(int(count)==1):
        doc_dict1=build_entire_doc_dict_using_championlist(query,index,posting_list,champion_list)
    elif(int(count)==2):
        doc_dict1=build_entire_doc_dict_using_championlist(query,index,posting_list,champion_list)
        doc_dict2=build_entire_doc_dict(query,index,posting_list)
    elif(int(count)==3):
        doc_dict1=build_entire_doc_dict_using_championlist(query,index,posting_list,champion_list)
        doc_dict2=build_entire_doc_dict_using_championlist(query,index0,posting_list0,champion_list)
    else:
        doc_dict1=build_entire_doc_dict_using_championlist_choice(query,index,posting_list,champion_list,1)
        doc_dict2=build_entire_doc_dict_using_championlist_choice(query,index,posting_list,champion_list,0)
    
    doc_ranking1={}
    for docid,docid_vector in doc_dict1.items():
        calculate_score_for_a_document(docid,docid_vector,query_vector,doc_ranking1)
    doc_ranking1={k: v for k, v in sorted(doc_ranking1.items(), key=lambda item: item[1],reverse=True)}
    if(k>len(doc_ranking1.keys())):
        k=len(doc_ranking1.keys())
    first_k=list(doc_ranking1.keys())[0:k]
    df=pd.DataFrame(columns=[['DOCID','Title','Score']])
    for key in first_k:
        df.loc[len(df.index)]=[key,title[key],doc_ranking1[key]]
    print("-----------------")
    print(df)
    print("-----------------")
    end1=time.time()
    print(end1-begin)
    
    if(int(count)!=1):
        doc_ranking2={}
        for docid,docid_vector in doc_dict2.items():
            calculate_score_for_a_document(docid,docid_vector,query_vector,doc_ranking2)
        doc_ranking2={k: v for k, v in sorted(doc_ranking2.items(), key=lambda item: item[1],reverse=True)}
        if(k>len(doc_ranking2.keys())):
            k=len(doc_ranking2.keys())
        first_k=list(doc_ranking2.keys())[0:k]
        df1=pd.DataFrame(columns=[['DOCID','Title','Score']])
        for key in first_k:
            df1.loc[len(df1.index)]=[key,title[key],doc_ranking2[key]]
        print("-----------------")
        print(df1)
        print("-----------------")
        end=time.time()
        print(end-end1)
    else:
        pass

while(True):
    calculate_all(10)
# In[218]





