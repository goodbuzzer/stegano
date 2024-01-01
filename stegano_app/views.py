from django.shortcuts import render
from django.conf import settings
import os
import random
import stepic
from PIL import Image # importing the Image module from the PIL library.
import io

# Create your views here.

def index(request):
    return render(request, 'index.html')
    
# get the path of a random file in a folder
def random_file(folder):
    fichiers =  [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
    if not fichiers:
        return ""
    fichier_au_hasard = random.choice(fichiers)
    chemin_complet = os.path.join(folder, fichier_au_hasard)
    return chemin_complet


def hide_text_in_image(image, text):
    data = text.encode('utf-8')
    '''encode('utf-8') on a string, it translates the human-readable 
    characters into a sequence of bytes using the UTF-8 encoding.
     The result is a bytes object in Python.'''
    return stepic.encode(image, data)
#stepic.encode method is called to hide these bytes within the image

def encryption_view(request):
    media_root = settings.MEDIA_ROOT
    message = ''
    if request.method == 'POST':
        text = request.POST['text']
        categorie = request.POST['categorie']
        dossier_categorie = media_root + categorie
        image_file = random_file(dossier_categorie)
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':  # checks whether the image format is not PNG.
            image = image.convert('RGBA')
            # image is converted to RGBA mode if it's not already
            # This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            # A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # hide text in image
        new_image = hide_text_in_image(image, text)

        # save the new image in a project folder
        image_name = os.path.splitext(image_file)[0]
        image_path = image_name + '_encrypte' + '.png'
        save_image(image_path, new_image)
        
        image_link = settings.MEDIA_URL + categorie + '/' + os.path.basename(image_name) + '_encrypte' + '.png'
        return render(request, 'succes_encryption.html', {'image_link': image_link})
    else:
        return render(request, 'encryption.html')
        
# encrypt an image 
def encryption_image_view(request):
    media_root = settings.MEDIA_ROOT
    message = ''
    if request.method == 'POST':
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':  # checks whether the image format is not PNG.
            image = image.convert('RGBA')
            # image is converted to RGBA mode if it's not already
            # This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            # A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # hide text in image
        new_image = hide_text_in_image(image, text)
        
        # save the new image in a project folder
        image_name = os.path.splitext(image_file.name)[0]
        image_path = media_root + image_name + '_encrypte' + '.png'
        save_image(image_path, new_image)

        image_link = settings.MEDIA_URL + os.path.basename(image_name) + '_encrypte' + '.png'
        return render(request, 'succes_encryption.html', {'image_link': image_link})
    else:
        return render(request, 'encryption.html')
    
# save an image in a file
def save_image(image_path, image):
    image.save(image_path, format="PNG")

def decryption_view(request):
    message = ''
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':#checks whether the image format is not PNG.
            image = image.convert('RGBA')
            #image is converted to RGBA mode if it's not already
            #This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            #A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # extract message from image
        message = extract_text_from_image(image)
        return render(request, 'succes_decryption.html', {'message' : message})
    else:
        return render(request, 'decryption.html')

def extract_text_from_image(image):
    data = stepic.decode(image)
    # uses the decode function from the stepic library to extract the
    # hidden data from the given image. This hidden data is
    # typically stored as bytes.
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data
