from django.shortcuts import render
import json
import os
from django.conf import settings
import pandas as pd
from sklearn import model_selection, svm, naive_bayes, metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def task1_view(request):
    # Check if the results file exists
    results_path = os.path.join(settings.MEDIA_ROOT, 'model_results.json')
    
    if os.path.exists(results_path):
        try:
            with open(results_path, 'r') as f:
                results = json.load(f)
            print("Loaded results from JSON file.")
            # Load confusion matrices and accuracies from the JSON file
            svm_accuracy = results.get('svm_accuracy', 0)
            nb_accuracy = results.get('nb_accuracy', 0)
            svm_conf_matrix = results.get('svm_conf_matrix', '')
            nb_conf_matrix = results.get('nb_conf_matrix', '')
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return render(request, 'users/task1.html', {'error': 'Failed to load previous results.'})
    else:
        try:
            print("Reading processed data and labels...")
            path1 = os.path.join(settings.MEDIA_ROOT, 'processed_data_vol2.csv')
            path2 = os.path.join(settings.MEDIA_ROOT, 'class.csv')
            dp = pd.read_csv(path1, encoding='cp1252')
            dc = pd.read_csv(path2, encoding='cp1252')
            print("Data read successfully.")
        except Exception as e:
            print(f"Error reading data: {e}")
            return render(request, 'users/task1.html', {'error': 'Failed to read data.'})

        # Perform the calculations and training
        try:
            print("Splitting data into training and testing sets...")
            Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(dp['text_final'], dc['class'], test_size=0.3)
            print("Data split successfully.")
        except Exception as e:
            print(f"Error splitting data: {e}")

        try:
            print("Encoding labels...")
            Encoder = LabelEncoder()
            Train_Y = Encoder.fit_transform(Train_Y)
            Test_Y = Encoder.fit_transform(Test_Y)
            print("Labels encoded successfully.")
        except Exception as e:
            print(f"Error encoding labels: {e}")

        try:
            print("Vectorizing text data...")
            Tfidf_vect = TfidfVectorizer()
            Tfidf_vect.fit(dp['text_final'])
            Train_X_Tfidf = Tfidf_vect.transform(Train_X)
            Test_X_Tfidf = Tfidf_vect.transform(Test_X)
            print("Text data vectorized successfully.")
        except Exception as e:
            print(f"Error vectorizing text data: {e}")

        try:
            print("Training SVM model...")
            SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
            SVM.fit(Train_X_Tfidf, Train_Y)
            print("SVM model trained successfully.")
        except Exception as e:
            print(f"Error training SVM model: {e}")

        try:
            print("Training Naive Bayes model...")
            Naive = naive_bayes.MultinomialNB()
            Naive.fit(Train_X_Tfidf, Train_Y)
            print("Naive Bayes model trained successfully.")
        except Exception as e:
            print(f"Error training Naive Bayes model: {e}")

        try:
            print("Saving models to disk...")
            svm_filename = 'finalized_model_SVM.sav'
            nb_filename = 'finalized_model_NB.sav'
            pickle.dump(SVM, open(os.path.join(settings.MEDIA_ROOT, svm_filename), 'wb'))
            pickle.dump(Naive, open(os.path.join(settings.MEDIA_ROOT, nb_filename), 'wb'))
            print("Models saved successfully.")
        except Exception as e:
            print(f"Error saving models: {e}")

        try:
            print("Making predictions using SVM and Naive Bayes...")
            predictions_SVM = SVM.predict(Test_X_Tfidf)
            predictions_NB = Naive.predict(Test_X_Tfidf)
            print("Predictions made successfully.")
        except Exception as e:
            print(f"Error making predictions: {e}")

        try:
            print("Calculating accuracies...")
            svm_accuracy = accuracy_score(predictions_SVM, Test_Y) * 100
            nb_accuracy = accuracy_score(predictions_NB, Test_Y) * 100
            print(f"SVM Accuracy: {svm_accuracy}%")
            print(f"Naive Bayes Accuracy: {nb_accuracy}%")
        except Exception as e:
            print(f"Error calculating accuracies: {e}")

        try:
            print("Generating confusion matrices...")
            def generate_conf_matrix(model, predictions):
                mat = confusion_matrix(predictions, Test_Y)
                axis_labels = ['Hateful', 'Not Hateful']
                plt.figure(figsize=(6, 4))
                sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False,
                            xticklabels=axis_labels, yticklabels=axis_labels)
                plt.title(f"{model} Confusion Matrix")
                plt.xlabel('Predicted Categories')
                plt.ylabel('True Categories')
                plt.tight_layout()
                plt.savefig(os.path.join(settings.MEDIA_ROOT, f"{model}_confusion_matrix.png"))
            
            generate_conf_matrix("SVM", predictions_SVM)
            generate_conf_matrix("Naive_Bayes", predictions_NB)
            print("Confusion matrices generated successfully.")
        except Exception as e:
            print(f"Error generating confusion matrices: {e}")

        # Store results in the JSON file
        results = {
            'svm_accuracy': svm_accuracy,
            'nb_accuracy': nb_accuracy,
            'svm_conf_matrix': 'finalized_model_SVM_confusion_matrix.png',
            'nb_conf_matrix': 'finalized_model_NB_confusion_matrix.png',
        }
        try:
            with open(results_path, 'w') as f:
                json.dump(results, f)
            print("Results saved to JSON file.")
        except Exception as e:
            print(f"Error saving results to JSON: {e}")

    # Return the context to the template
    return render(request, 'users/task1.html', results)
