from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

@ensure_csrf_cookie
@require_GET
def csrf_view(request):
    return JsonResponse({"message": "CSRF cookie ready"})

@require_POST
def register_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({ "message": "Registration successful!"},status=201)
    return JsonResponse({"errors": {
            field: list(errors)
            for field, errors in form.errors.items()}},status=400)

@require_POST
def login_view(request):
    u = request.POST.get("username")
    p = request.POST.get("password")

    user = authenticate(request,username=u,password=p)
    if user is not None:
        login(request,user)
        return JsonResponse({"message":"Login successful","user":{"id":user.id,"username":user.username}})
    return JsonResponse({"error":"Invalid username or password!"},status=400)

@require_GET
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"user":{"id":request.user.id,"username":request.user.username}})
    return JsonResponse({"user":None})

    



# Create your views here.
