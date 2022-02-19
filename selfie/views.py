from FCN import Run
from django.shortcuts import render
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
    run = Run()
    model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'eCybermission/trained_models/(Model:FCN-Dense-Layers)_(Epoch:01)_(Loss:0.97)_(Accuracy:1.00).h5')
    image_directory_path = os.path.join(os.path.dirname(__file__), '..', '..', 'eCybermission/FCN/images')
    prediction = run.use_model(base64string=base64string, MODEL_PATH=model_path, model_type='FCN-Dense-Layers', image_directory_path=image_directory_path)
    return JsonResponse({"prediction":prediction})