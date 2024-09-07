from rest_framework import generics, serializers
from .models import Project
from .serializers import GithubProjectSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = GithubProjectSerializer
# Compare this snippet from projects/urls.py:

from django.shortcuts import get_object_or_404, render

def admin(request):
    return render(request, 'admin.html')

def index(request):
    return render(request, 'index.html')



@csrf_exempt
@require_http_methods(["DELETE"])
def project_delete(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return JsonResponse({"message": f"Project with id {project_id} has been successfully deleted."}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"error": f"Project with id {project_id} does not exist or has already been deleted."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def save_project(request):
    if request.method == 'POST':
        # Assuming you have a form with fields 'name' and 'description'
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Create a new Project object and save it to the database
        project = Project(name=name, description=description)
        project.save()
        
        # Optionally, you can return a response indicating success
        return HttpResponse('Project saved successfully.')
    
    # If the request method is not POST, you can handle it accordingly
    else:
        return HttpResponse('Invalid request method.')
    


@api_view(['POST'])
def add_items(request):
    item = GithubProjectSerializer(data=request.data)
    
    # validating for already existing data
    if Project.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    print('This data already existsdeemesiiiii')
    if item.is_valid():
        item.save()
        return JsonResponse(item.data, status=201)
    else:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    