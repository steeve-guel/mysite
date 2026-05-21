from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import numpy as np
import joblib 
from PIL import Image 

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'svm_prediction_images.joblib')
svm_model = joblib.load(MODEL_PATH)

CLASSES = ['Meuble', 'Voiture'] 


IMAGE_SIZE = (128, 128) 

def index(request):
    if request.method == 'POST' and request.FILES['image_file']:
       
        myfile = request.FILES['image_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        file_path = fs.path(filename)

        img = Image.open(file_path).convert("L").resize(IMAGE_SIZE)
        
       
        img_array = np.array(img)
        
        
        flattened_img = img_array.flatten().reshape(1, -1)

     
        prediction = svm_model.predict(flattened_img)
        
       
        class_index = int(prediction[0])
        
        try:
            resultat = CLASSES[class_index]
        except IndexError:
            resultat = f"Classe inconnue (Index : {class_index})"

        return render(request, 'predictor/index.html', {
            'uploaded_file_url': uploaded_file_url,
            'resultat': resultat,
        })

    return render(request, 'predictor/index.html')