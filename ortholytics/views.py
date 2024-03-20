from django.shortcuts import render, redirect
# from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from .models import *
### new added 
from django.http import HttpResponse
from django.http import JsonResponse
import pymongo
import pandas as pd
import numpy as np
import json


from .models import collection  ## pymongo db collection
import pandas as pd
from datetime import datetime
import assemblyai as aai

# Replace with your API key

def diarization(audio_file):
    print(audio_file)
    print("Dekho mai yaha aayaaaaaaaaa!")
    aai.settings.api_key = "0ca2f9180fdc4dfeb7e2831d8201da1b"
    FILE_URL=audio_file
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
    FILE_URL,
    config=config
    )
    text=""
    for utterance in transcript.utterances:
        text+=f"Speaker {utterance.speaker}: {utterance.text}"
    return text

def index(request):
    if request.method == 'POST':
        if request.FILES['audioFile']:
            audio_file = request.FILES['audioFile']
            print(audio_file)
            with open('temp_audio.wav', 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            print(audio_file.name)
            conversation=diarization('temp_audio.wav')
            return JsonResponse({'conversation': conversation})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    context={
    }
    return render(request, "home.html", context)