from django.shortcuts import render
import tensorflow as tf
from django.utils.safestring import mark_safe
# Create your views here.
def index(request):
    return render(request, 'index.html')


from django.shortcuts import render
from .forms import ImageUploadForm
import os
from django.conf import settings

def deepfakeimage(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['image']
            file_name = "uploaded_image.jpg"
            file_path = os.path.join(settings.STATICFILES_DIRS[0], file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            model = tf.saved_model.load('./models/my_model')
            # Load the image
            image_string = tf.io.read_file('./static/uploaded_image.jpg')
            image_decoded = tf.image.decode_jpeg(image_string, channels=3)  # replace with decode_png if it's a PNG image
            image_resized = tf.image.resize(image_decoded, [128, 128])  # replace with the size your model expects
            image_normalized = image_resized / 255.0  # normalize to [0,1] range

            # Add a batch dimension
            input_data = tf.expand_dims(image_normalized, 0)

            # Use the model
            predictions = model(input_data)

            print('pred is ')
            value = predictions.numpy()[0][0]
            print(value)
            #print(predictions)

            

            if value < 0.5:
                output = {
                "output" : mark_safe("This image is <span style='color: #FF0000;'>FAKE</span>"),
                "value" : value
                }
                print('fake')
            else:
                output = {
                "output" : mark_safe("This image is <span style='color: #00FF00;'>REAL</span>"),
                "value" : value
                }
                print('real')


            print('success')



            return render(request, 'deepfakeimage.html',output)
        
        print('not valid')
    else:
        form = ImageUploadForm()
    return render(request, 'deepfakeimage.html', {'form': form})


from django.shortcuts import render
from .forms import AudioUploadForm
import os
from django.conf import settings
from joblib import load
import librosa
import numpy as np

def deepfakeaudio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['audio']
            file_name = "uploaded_audio.mp3"  # hardcoded filename
            file_path = os.path.join(settings.STATICFILES_DIRS[0], file_name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            

            model = load('./models/audio_model.joblib')
            audio, sample_rate = librosa.load('./static/uploaded_audio.mp3')
            features = extract_features([audio], [sample_rate])
            predictions = model.predict(features)
            print(predictions)

            if predictions < 0.5:
                output = {
                "output" : mark_safe("This Audio is <span style='color: #FF0000;'>FAKE</span>"),
                "value" : predictions
                }
                print('fake')
            else:
                output = {
                "output" : mark_safe("This Audio is <span style='color: #00FF00;'>REAL</span>"),
                "value" : predictions
                }
                print('real')


            print('success')
            return render(request, 'deepfakeaudio.html',output)
    else:
        form = AudioUploadForm()
    return render(request, 'deepfakeaudio.html', {'form': form})



def extract_features(audios, sample_rates):
    features = []
    for audio, sample_rate in zip(audios, sample_rates):
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
        mfccs_scaled = np.mean(mfccs.T, axis=0)
        features.append(mfccs_scaled)
    return features