import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pickle 
import tkinter as tk
from django.conf import settings
import os


svm_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_SVM.sav')
nb_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_NB.sav')

# load the model SVM from disk
try:
    print("Loading SVM model...")
    loaded_model_svm = pickle.load(open(svm_path, 'rb'))
    print("SVM model loaded successfully.")
except Exception as e:
    print(f"Error loading SVM model: {e}")

# load the model NB from disk
try:
    print("Loading Naive Bayes model...")
    loaded_model_nb = pickle.load(open(nb_path, 'rb'))
    print("Naive Bayes model loaded successfully.")
except Exception as e:
    print(f"Error loading Naive Bayes model: {e}")

# read the processed data
data_path = os.path.join(settings.MEDIA_ROOT,'processed_data_vol2.csv')

try:
    print("Reading the data...")
    dp = pd.read_csv(data_path, encoding='cp1252')
    print("Data read successfully.")
except Exception as e:
    print(f"Error reading data: {e}")

# With Tfidf Vectorizer
try:
    print("Fitting the Tfidf Vectorizer...")
    Tfidf_vect = TfidfVectorizer()
    Tfidf_vect.fit(dp['text_final'])
    print("Tfidf Vectorizer fitted successfully.")
except Exception as e:
    print(f"Error fitting Tfidf Vectorizer: {e}")

def create_gui():
    # GUI
    try:
        print("Creating GUI...")
        root = tk.Tk()

        canvas = tk.Canvas(root, width=1200, height=720, relief='raised')
        canvas.pack()

        label = tk.Label(root, text='Hate-Speech Recognizer')
        label.config(font=('helvetica', 28, 'bold'))
        canvas.create_window(600, 155, window=label)

        label = tk.Label(root, text='Enter sentence:')
        label.config(font=('helvetica', 24, 'bold'))
        canvas.create_window(600, 250, window=label)

        entry = tk.Entry(root, font=('helvetica', 18))
        canvas.create_window(600, 300, window=entry)

        def formatPrediction(model, output, index, user_input):
            label = tk.Label(root, text=f"'{user_input}' is recognized as: ", font=('helvetica', 24), width=70, height=3)
            canvas.create_window(600, 440, window=label)

            labelPred = tk.Label(root, text="", width=20, height=3, font=('helvetica', 18))

            if (output == 0):
                labelPred.config(text=f"{model}: Hateful")
                labelPred.config(bg="red")
            else:
                labelPred.config(text=f"{model}: Not Hateful")
                labelPred.config(bg="green")

            canvas.create_window(600, (480 + (55 * index)), window=labelPred)

        def predictInput():
            user_input = entry.get()  # get input sentence
            new_input = [user_input]  # put input sentence in array format (to use in prediction)
            new_input_Tfidf = Tfidf_vect.transform(new_input)  # vectorize input

            # SVM prediction
            new_output_svm = loaded_model_svm.predict(new_input_Tfidf)
            # Naive Bayes prediction
            new_output_nb = loaded_model_nb.predict(new_input_Tfidf)

            # configure the prediction labels
            formatPrediction("SVM", new_output_svm, 1, user_input)
            formatPrediction("Naive Bayes", new_output_nb, 2, user_input)

        button = tk.Button(text='Get Predictions', command=predictInput, bg='white', fg='black', font=('helvetica', 19, 'bold'))
        canvas.create_window(600, 350, window=button)

        root.mainloop()
        print("GUI created successfully.")
    except Exception as e:
        print(f"Error creating GUI: {e}")

def main_menu():
    try:
        print("Creating main menu...")
        main_root = tk.Tk()
        main_root.geometry("400x200")

        def open_gui():
            main_root.destroy()
            create_gui()

        open_button = tk.Button(main_root, text='Open Hate-Speech Recognizer', command=open_gui, bg='white', fg='black', font=('helvetica', 19, 'bold'))
        open_button.pack(pady=60)

        main_root.mainloop()
        print("Main menu created successfully.")
    except Exception as e:
        print(f"Error creating main menu: {e}")

if __name__ == "__main__":
    print("Starting application...")
    main_menu()
