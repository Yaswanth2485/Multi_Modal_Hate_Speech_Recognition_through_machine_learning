from django.shortcuts import render,redirect, redirect, get_object_or_404
from django.contrib import messages
from .models import registrationmodel
from .forms import registrationmodelmodelform
from django.utils.timezone import now
import re
import qrcode
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
import os
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from datetime import datetime,timedelta 


# Create your views here.
#------------------------------------------------------------------main page-------------------------------------------------------

def basefunction(request):
    return render(request,'base.html')
    
# ----------------------------------------------------------------user login & logout---------------------------------------------------

def userlogin(request):
    return render(request,'userlogin.html') 

def userlogout(request):
    return render(request,'base.html')

#  ----------------------------------------------------------------user registration-----------------------------------------------------

def registercheck(request):
    if request.method == 'POST':
        form = registrationmodelmodelform(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            if registrationmodel.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already registered.')
            elif registrationmodel.objects.filter(mobile=mobile).exists():
                messages.warning(request, 'Mobile number is already registered.')
            else:
                instance = form.save(commit=False)
                instance.status = 'waiting'
                instance.save()
                messages.success(request, 'Account created successfully! Wait for activation by admin.')
                form = registrationmodelmodelform()  # Reset the form
                return render(request, 'studentregistration.html', {'form': form})
        else:
            print(form.errors)
            messages.warning(request, 'Please correct the errors below.')
    else:
        form = registrationmodelmodelform()
    return render(request, 'studentregistration.html', {'form': form})

# --------------------------------------------------------------------user login check-----------------------------------------------

def userlogincheck(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        try:
            user = registrationmodel.objects.get(email__iexact=email)
            print(f"Debug: Retrieved user status: {user.status}")
            if user.status.lower() == 'blocked':
                messages.error(request, 'Your account is blocked. Please contact our admin team.')
                return render(request, 'userlogin.html')
            if user.status.lower() != 'activated':
                messages.warning(request, 'Your account is not active. Please wait for admin approval.')
                return render(request, 'userlogin.html')
            if user.password == password:
                request.session['email'] = user.email
                request.session['name'] = user.name
                user.last_login = now()
                user.save()  
                print(f"Debug: Logged-in user email: {request.session['email']}")
                print(f"Debug: Logged-in user name: {request.session['name']}")
                print(f"Debug: Session data: {request.session.items()}")

                return render(request, 'users/userhome.html', {'user': user})
            else:
                messages.error(request, 'Invalid password. Please try again.')
                return render(request, 'userlogin.html')
        except registrationmodel.DoesNotExist:
            messages.error(request, 'Email is not registered. Please sign up first.')
            return render(request, 'userlogin.html')
    return render(request, 'userlogin.html')

# -------------------------------------------------------------user home & profile & profile update-------------------------------------------

def user_home(request):
    if 'email' not in request.session:
        return redirect('userlogin')
    email = request.session.get('email')
    user = registrationmodel.objects.get(email=email)
    return render(request, 'users/userhome.html', {'user': user})  

def user_profile(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'You need to log in first.')
        return redirect('userlogin')
    try:
        user = registrationmodel.objects.get(email=email)
        return render(request, 'users/profile.html', {'user': user})
    except registrationmodel.DoesNotExist:      
        return redirect('userlogin')

def update_profile(request):
    email = request.session.get('email')
    try:
        user = registrationmodel.objects.get(email=email)
    except registrationmodel.DoesNotExist:       
        return redirect('userlogin')
    if request.method == 'POST':
        form = registrationmodelmodelform(request.POST, instance=user)
        if form.is_valid():
            form.fields.pop('password', None)
            form.fields.pop('confirm_password', None)
            form.save()
            messages.success(request, 'Profile updated successfully! login with the new updated email.!')
            return redirect('userprofile')
        else:
            messages.warning(request, 'Please correct the errors below.')
    else:
        form = registrationmodelmodelform(instance=user)
        form.fields.pop('password', None)
        form.fields.pop('confirm_password', None)
    return render(request, 'users/profileupdate.html', {'form': form})




def Task1(request):
    return render(request, 'users/task1.html')

def ConfusionMatrice(request):
    return render(request, 'users/confusion_matrix.html')



from django.shortcuts import render
from django.http import HttpResponse
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from .forms import HateSpeechForm
from django.conf import settings
import os

svm_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_SVM.sav')
nb_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_NB.sav')
# Load the models and vectorizer
loaded_model_svm = pickle.load(open(svm_path, 'rb'))
loaded_model_nb = pickle.load(open(nb_path, 'rb'))


data_path = os.path.join(settings.MEDIA_ROOT,'processed_data_vol2.csv')
# Load the processed data to fit the vectorizer
dp = pd.read_csv(data_path, encoding='cp1252')

# Fit the Tfidf Vectorizer
Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(dp['text_final'])

def hate_speech_predictor(request):
    if request.method == 'POST':
        form = HateSpeechForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['sentence']
            new_input = [user_input]
            new_input_Tfidf = Tfidf_vect.transform(new_input)

            # SVM prediction
            new_output_svm = loaded_model_svm.predict(new_input_Tfidf)
            # Naive Bayes prediction
            new_output_nb = loaded_model_nb.predict(new_input_Tfidf)

            predictions = {
                'user_input': user_input,
                'svm_prediction': 'Hateful' if new_output_svm == 0 else 'Not Hateful',
                'nb_prediction': 'Hateful' if new_output_nb == 0 else 'Not Hateful',
            }

            return render(request, 'users/hate_speech_result.html', {'predictions': predictions})
    else:
        form = HateSpeechForm()

    return render(request, 'users/hate_speech_form.html', {'form': form})


def hate_speech_predictor_audio(request):
    if request.method == 'POST':     
        user_input = request.POST.get("msg") 
        new_input = [user_input]
        new_input_Tfidf = Tfidf_vect.transform(new_input)

        # SVM prediction
        new_output_svm = loaded_model_svm.predict(new_input_Tfidf)
        # Naive Bayes prediction
        new_output_nb = loaded_model_nb.predict(new_input_Tfidf)

        predictions = {
            'user_input': user_input,
            'svm_prediction': 'Hateful' if new_output_svm == 0 else 'Not Hateful',
            'nb_prediction': 'Hateful' if new_output_nb == 0 else 'Not Hateful',
        }

        return render(request, 'users/hate_speech_audio_result.html', {'predictions': predictions})
    else:
        form = HateSpeechForm()

    return render(request, 'users/hate_speech_result_audio.html', {'form': form})