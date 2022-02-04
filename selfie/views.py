.from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    pass

def name(request, name):
    the_string = f"Hello {name}!"
    print(the_string)
    return JsonResponse({"message":the_string})

@csrf_exempt
def image(request):
    base64string = json.loads(request.body)
    print(base64string)
    #print(f"The data is {data}")
    #base64string = data.get("content")
    stringlength = len(base64string) - len("data:image/png;base64,")
    sizeInBytes = (stringlength * 3/4) - base64string.count('=', -2)
    print(round(sizeInBytes))
    return JsonResponse({"size":round(sizeInBytes)})
