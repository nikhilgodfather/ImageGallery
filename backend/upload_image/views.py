# views.py
from django.http import JsonResponse
from .models import Image , ImageDetail
from django.middleware.csrf import get_token
from .serializers import ImageSerializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from uuid import uuid4
import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .serializers import ImageSerializers
from django.shortcuts import get_object_or_404

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

import json
from django.http import JsonResponse
from .models import Image

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_image(request):
    if request.method == 'POST' and request.FILES:
        images = request.FILES.getlist('images')  # Get list of uploaded images
        caption = request.data.get('caption', '')  # Get caption from the request data

        # Create an empty list to store image data
        image_data = []

        # Create an Image object for each uploaded image
        for image_file in images:
            image = Image.objects.create(file=image_file, caption=caption)
            # Append the URL of the image file to the image data list
            image_data.append(image.file.url)

        # Get the ID of the newest created Image object
        latest_image = Image.objects.latest('id')
        current_id = latest_image.id if latest_image else 0

        # Create a dictionary for the new entry with an auto-incremented primary key
        new_entry = {
            'id': current_id + 1,
            'caption': caption,
            'images': image_data
        }

        with open('data.json', 'r') as file:
            current_data = json.load(file)
        
        current_data.append(new_entry)

        # Write the updated data back to the JSON file
        with open('data.json', 'w') as file:
            json.dump(current_data, file, indent=4)

        return JsonResponse({'message': 'Images uploaded successfully', 'image_data': image_data})
    else:
        return JsonResponse({'error': 'No images provided'}, status=400)

@api_view(['GET'])
def get_images(request):
    try:
        # Read the contents of the data.json file
        with open('data.json', 'r') as file:
                data = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        data = []

    # Return the parsed JSON data as a JSON response
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def deleteImage(request, id):
    # Read the JSON file
    with open('data.json') as f:
        data = json.load(f)
    

    # Find the index of the entry with the specified ID
    index_to_delete = None
    for index, entry in enumerate(data):
        if entry['id'] == id:
            index_images = entry["images"]
            index_to_delete = index
            break
    for image in index_images:
       mage_path = os.path.join('media\images', image[14:])
       ImageObject = Image.objects.filter(file=image[7:]).delete()
       if ImageObject:
            if os.path.exists(mage_path):
                os.remove(mage_path)
                print('Images Deleted Successfully')
            else:
                pass
       else:
           pass
           
        
    # Check if the entry with the specified ID was found
    if index_to_delete is not None:
        # Delete the entry with the specified ID from the list
        del data[index_to_delete]
        
        # Write the updated data back to the JSON file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        # Return a JSON response indicating success
        return JsonResponse({'message': f'Entry with ID {id} deleted successfully.'})
    else:
        # Return a JSON response indicating that the ID was not found in the data
        return JsonResponse({'error': f'Entry with ID {id} not found.'}, status=404)
    
@api_view(['GET'])
def updateImage(request, id):
    # Read data from data.json file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Find the image entry with the specified id
    image_entry = None
    for image in data:
        if image['id'] == id:
            image_entry = image
            break
    # If the image entry is found, return its details
    if image_entry:
        return JsonResponse(image_entry)
    else:
        return JsonResponse({'error': 'Image not found'}, status=404)
    
@api_view(['POST'])
def AddonImage(request, id):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        caption = request.data.get('caption', '')
        # Create an Image object
        image_object = Image.objects.create(file=image_file, caption=caption)
        
        # Update the data.json file
        with open('data.json', 'r+') as file:
            data = json.load(file)
            for item in data:
                if item['id'] == id:
                    item['images'].append(image_object.file.url)
                    item["caption"] = caption
                    break
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        
        return JsonResponse({'message': 'Image uploaded successfully'}, status=200)
    elif(request.method == 'POST'):
        caption = request.data.get('caption', '')
        with open('data.json', 'r+') as file:
            data = json.load(file)
            for item in data:
                if item['id'] == id:
                    item["caption"] = caption
                    break
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        
        return JsonResponse({'message': 'Image uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
import os

@api_view(['POST'])
def DeleteSingleImage(request, id):
    if request.method == 'POST':
        # Retrieve the URL from the request body
        url = request.data.get('url')
        
        # Load the JSON data from the file
        with open('data.json', 'r') as file:
            data = json.load(file)

        # Iterate over the data to find the image with the specified ID
        for item in data:
            if item["id"] == id:
                # Remove the URL from the images list
                item["images"].remove(url)
                break
        
        # Write the updated data back to the file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        # Delete the corresponding Image object from the database
        image_object = Image.objects.filter(file=url[7:]).first()
        if image_object:
            # Delete the image file from the server's storage location
            image_path = os.path.join('media', image_object.file.name)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Image file '{image_path}' deleted successfully.")
            else:
                print(f"Image file '{image_path}' does not exist.")
            
            # Delete the Image object from the database
            image_object.delete()
            print(f"Image object '{image_object}' deleted successfully.")
        else:
            pass
        
        return JsonResponse({'message': 'Image path and object deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
