#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import scikit learn and numpy libraries required for this code
import glob
import sys
import numpy as np
import os
from sklearn.feature_extraction.text import *
from sklearn.metrics.pairwise import cosine_similarity

print 'Enter the path of folder:'
doc_path=raw_input()
files = glob.glob(doc_path)	#stores paths of all files as a list

tfidf_vectorizer = TfidfVectorizer('filename',stop_words='english',min_df=0.0,use_idf=True)	#scikit function to make document vectors
corpus_tfidf_matrix = tfidf_vectorizer.fit_transform(files)	#scikit function to calculate tf-idf matrix


tot_words=len(tfidf_vectorizer.vocabulary_)

print 'Enter the path of query document:'
qinp=raw_input()
q=[qinp]
test=tfidf_vectorizer.transform(q)	#form the vector from query document
test_qur= test.todense()

test_qur_list=np.array(test_qur).tolist()
query_vector = [0 for j in range(pow(2,tot_words))]

corpus_tfidf_mat=corpus_tfidf_matrix.todense()	#matrix form of tf-idf matrix calculated above

minterm=[]		#list to store minterm unit vectors

corpus_tfidf=np.array(corpus_tfidf_mat).tolist()

print(len(tfidf_vectorizer.vocabulary_))

for key,value in sorted(tfidf_vectorizer.vocabulary_.items()):	#print the vocabulary of corpus
	print(key)

print('--------------------------------------------------------------------------------------------')

#Construct the minterms of GVSM vector space
for i in corpus_tfidf:

	temp_l=i
	val=0
	cn=0

	for k in temp_l:
		if k > 0 :	
			val=val+pow(2,cn)
		cn=cn+1
	minterm=minterm+[val]			

unit_vectors=[]
p=[]
size_of_minterms=pow(2,(tot_words))	#size of GVSM vector space is 2^total_words

#Calculate the index term vectors as linear combinations of minterm vectors
for i in range(0,tot_words):
	tmp_unit_vector = [0 for j in range(pow(2,tot_words))]
	cnt=0
	for k in corpus_tfidf:
		cn=0
		for l in k:
			if i == cn and l >0:
				tmp_unit_vector[minterm[cnt]]=tmp_unit_vector[minterm[cnt]]+l
			cn=cn+1	
		cnt=cnt+1
	magnitude=np.linalg.norm(tmp_unit_vector)
	myArr=np.array(tmp_unit_vector)
	newArr=myArr/magnitude
	p.append(newArr)


queryVector=np.zeros(pow(2,tot_words))
sim=[]
count_file=0

#loop constructs query vector from query doc in GVSM vector space as linear combination of minterm vectors
for doc in test_qur_list:
	count=0 #keeps count of index terms

	for value in doc:
		query_vector+=(value*p[count])
		count=count+1

#this loop constructs document in the GVSM vector space as linear combination of minterm vectors and calculates cosine similarity
for doc in corpus_tfidf:

	docVector=np.zeros(pow(2,tot_words))
	count=0 #keeps count of index terms

	for value in doc:
		docVector+=(value*p[count]) #product of tfidf value from matrix and nomrmalised term vectors from p
		count=count+1

	sim.append((cosine_similarity(query_vector,docVector)[0][0],os.path.basename(files[count_file]))) #cosine similarity
	count_file+=1

#sort the documents based on their similarity from highest to lowest similarity order
sim.sort(reverse=True)

#print the documents' ranking
for s in sim:
	print(s)
