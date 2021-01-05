import pandas as pd
import numpy as np
import os
## for processing
import re
import nltk
## for bag-of-words
from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing
## model & processing libraries
from sklearn import feature_selection
from sklearn.linear_model import LogisticRegressionCV
from sklearn import metrics
from sklearn import utils
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import multiprocessing
import pickle
## DB accesses
import sqlite3 as sq

from src.recommendation_engine.feature_engineering import process_data, create_embeddings

MODEL_PATH = "models/nlp"
MODEL_EMBEDDINGS_PATH = os.path.join(MODEL_PATH, 'similarity_embeddings')
CUISINE_CLASSES = ['brazilian','british','cajun_creole','chinese','filipino','french','greek','indian','irish','italian','jamaican','japanese','korean','mexican','moroccan','russian','southern_us','spanish','thai','vietnamese']
os.makedirs(MODEL_PATH, exist_ok=True)
os.makedirs(MODEL_EMBEDDINGS_PATH, exist_ok=True)

## Save to file in the current working directory
def save_pkl(file, pkl_filename):
    with open(pkl_filename, 'wb') as pkl_file:
        pickle.dump(file, pkl_file)

def compute_performances(predicted, predicted_prob, y_test):
    
    classes = np.unique(y_test)
    y_test_array = pd.get_dummies(y_test, drop_first=False).values

    ## Accuracy, Precision, Recall
    accuracy = metrics.accuracy_score(y_test, predicted)
    balance_accuracy = metrics.balanced_accuracy_score(y_test, predicted)
    auc = metrics.roc_auc_score(y_test, predicted_prob, 
                                multi_class="ovr")
    print("Balanced Accuracy:",  round(balance_accuracy,2))
    print("Accuracy:",  round(accuracy,2))
    print("Auc:", round(auc,2))
    print("Detail:")
    print(metrics.classification_report(y_test, predicted))

    '''## Plot confusion matrix
    cm = metrics.confusion_matrix(y_test, predicted)
    fig, ax = plt.subplots(figsize=(10,10), dpi=100)
    sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues, 
                cbar=False)
    ax.set(xlabel="Pred", ylabel="True", xticklabels=classes, 
           yticklabels=classes, title="Confusion matrix")
    plt.yticks(rotation=0)

    fig, ax = plt.subplots(figsize=(10,10), dpi=100, nrows=1, ncols=2)
    ## Plot roc
    for i in range(len(classes)):
        fpr, tpr, thresholds = metrics.roc_curve(y_test_array[:,i],  
                               predicted_prob[:,i])
        ax[0].plot(fpr, tpr, lw=3, 
                  label='{0} (area={1:0.2f})'.format(classes[i], 
                                  metrics.auc(fpr, tpr))
                   )
    ax[0].plot([0,1], [0,1], color='navy', lw=3, linestyle='--')
    ax[0].set(xlim=[-0.05,1.0], ylim=[0.0,1.05], 
              xlabel='False Positive Rate', 
              ylabel="True Positive Rate (Recall)", 
              title="Receiver operating characteristic")
    ax[0].legend(loc="lower right")
    ax[0].grid(True)

    ## Plot precision-recall curve
    for i in range(len(classes)):
        precision, recall, thresholds = metrics.precision_recall_curve(
                     y_test_array[:,i], predicted_prob[:,i])
        ax[1].plot(recall, precision, lw=3, 
                   label='{0} (area={1:0.2f})'.format(classes[i], 
                                      metrics.auc(recall, precision))
                  )
    ax[1].set(xlim=[0.0,1.05], ylim=[0.0,1.05], xlabel='Recall', 
              ylabel="Precision", title="Precision-Recall curve")
    ax[1].legend(loc="best")
    ax[1].grid(True)
    plt.show()'''

def create_model_cuisine_predictions():
    ## Process data
    dataset = process_data()

    ## Create embeddings
    vectorizer = feature_extraction.text.TfidfVectorizer() #create_embeddings(dataset)

    ## Model
    classifier = LogisticRegressionCV(cv=3,
                                      random_state=42,
                                      max_iter=300,
                                      n_jobs=-1,
                                      verbose=1) #naive_bayes.MultinomialNB()

    ## pipeline
    model = pipeline.Pipeline([("vectorizer", vectorizer),  
                                ("classifier", classifier)])

    ## Split the dataset
    dataset_train, dataset_test = model_selection.train_test_split(dataset, test_size=0.3, random_state=42)

    ## Create embeddings
    X_train = dataset_train['ingredients_query']; X_test = dataset_test['ingredients_query'];
    y_train = dataset_train['cuisine']; y_test = dataset_test['cuisine']; 

    ## train classifier
    model.fit(X_train, y_train)

    ## test
    predicted = model.predict(X_test)
    predicted_prob = model.predict_proba(X_test)

    ## Compute performance of the model
    compute_performances(predicted, predicted_prob, y_test)
    
    ## Save model and vectorizer to disk
    save_pkl(model, os.path.join(MODEL_PATH, "pickle_model.pkl"))

def d2v_embeddings(data):
    data = data['ingredients_query'].tolist()
    tagged_data = [TaggedDocument(words=row.split(), tags=[str(index)]) for index, row in enumerate(data)]

    max_epochs = 25
    vec_size = 20
    alpha = 0.025

    model_embedding = Doc2Vec(size=vec_size,
                        alpha=alpha, 
                        min_alpha=0.00025,
                        min_count=1,
                        dm =1)
  
    model_embedding.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model_embedding.train(tagged_data,
                    total_examples=model_embedding.corpus_count,
                    epochs=model_embedding.iter)
        # decrease the learning rate
        model_embedding.alpha -= 0.0002
        # fix the learning rate, no decay
        model_embedding.min_alpha = model_embedding.alpha
    
    return model_embedding

def train_model_embeddings():
    db = sq.connect('recipes.db')
    cursor = db.cursor()
    
    for cuisine in CUISINE_CLASSES:
        sql_query = "SELECT title, instructions, ingredients, ingredients_query FROM main_recipes WHERE cuisine = ?"
        data = pd.read_sql(sql_query, db, params=(cuisine,))
        
        model_embedding = d2v_embeddings(data)
        save_pkl(model_embedding, os.path.join(MODEL_EMBEDDINGS_PATH, f'd2v_{cuisine}.pkl'))