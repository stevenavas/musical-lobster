#Steven A Vasquez
#Date Created 07/24/2020


#To start program run in command line

#'streamlit run public_interest_tech.py'

#This web app was created to classify user inputs (their social needs) 
#to a specific non-profit organization is Atlantic City


#Import needed modules
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sqlite3 import Error
from sklearn.ensemble import RandomForestClassifier
import sqlite3
import nltk
import streamlit as st
nltk.download('stopwords')


# Read in data frame.
# Add extra repeat rows to make training set larger 
df = pd.read_csv('ac_sheet.csv')
df = pd.concat([df]*10000, ignore_index=True)

#nltk.download('stopwords')
stemmer = PorterStemmer()
words = stopwords.words("english")
df['cleaned'] = df['services'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

#Create vectorizer
vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
final_features = vectorizer.fit_transform(df['cleaned']).toarray() #Test vectorizer


#first we split our dataset into testing and training set:
# this block is to split the dataset into training and testing set 
X = df['cleaned']
Y = df['organizations']
# instead of doing these steps one at a time, we can use a pipeline to complete them all at once
pipeline = Pipeline([('vect', vectorizer), # #Word embedding
                     ('chi',  SelectKBest(chi2, k=300)), #Feature Selection
                     ('clf', RandomForestClassifier())]) #ML model type
# fitting our model and save it in a pickle for later use
model = pipeline.fit(X, Y)



#Change to text user input into pandas df 

def user_input_features():
    text           = st.text_input("What do you need help with")
    data           = {'services': text,
            }
    features       = pd.DataFrame(data, index=[0])
    #features       = features.apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
    return features

#The following lines of code uses streamlit to place previous code on a web app

user_inputs = user_input_features()

st.subheader('User Input parameters')
st.write(user_inputs)

prediction = model.predict(user_inputs)
prediction_proba = model.predict_proba(user_inputs)

st.subheader('Class labels and their corresponding index number')
st.write(Y.unique())

st.subheader('Prediction')
st.write(prediction)
#st.write(prediction)

st.subheader('Prediction Probability')
st.write(prediction_proba)



