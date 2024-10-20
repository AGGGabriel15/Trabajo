from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Carreras, Estudiantes

def index(request):
    if request.user.is_authenticated:

        list_estudiantes = Estudiantes.objects.all()
        return render(request, "tasks/index.html", {
            "list_estudiantes": list_estudiantes,
        })

    else:
        return HttpResponseRedirect(reverse("login"))    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/login.html", {
                "message": "Usuario o contraseña invalido!"
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "tasks/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Las contraseñas no coinciden."
            })
        print(password)
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasks/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "tasks/register.html")

@login_required    
def new_estudiante(request):
    if request.method == "POST":
        nombres = request.POST.get("nombre")
        apellidos = request.POST.get("apellido")
        carrera = request.POST.get("carrera")
        carnet = request.POST.get("carnet")

        list_carreras = Carreras.objects.all()

        if not nombres or not apellidos or not carrera or not carnet:
            return render(request, "tasks/nuevo.html", {
                "list_carreras":list_carreras,
                "message":"Ingrese los datos solicitados",
            })
        
        carreraData = Carreras.objects.get(carrera = carrera)

        newEstudiante = Estudiantes(
            nombre = nombres,
            apellido = apellidos,
            carrera_on = carreraData,
            carnet = carnet,
        )

        newEstudiante.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        list_carreras = Carreras.objects.all()
        return render(request, "tasks/nuevo.html", {
            "list_carreras":list_carreras,
        })

@login_required
def editar(request, id):
    estudiante = get_object_or_404(Estudiantes, pk=id)

    if request.method == "POST":
        nombres = request.POST.get("nombre")
        apellidos = request.POST.get("apellido")
        carrera = request.POST.get("carrera")
        carnet = request.POST.get("carnet")

        list_carreras = Carreras.objects.all()

        if not nombres or not apellidos or not carrera or not carnet:
            return render(request, "tasks/nuevo.html", {
                "list_carreras":list_carreras,
                "message":"Ingrese los datos solicitados",
            })
        
        carreraData = Carreras.objects.get(carrera = carrera)

        estudiante.nombre = nombres
        estudiante.apellido = apellidos
        estudiante.carrera_on = carreraData
        estudiante.carnet = carnet

        estudiante.save()

        return HttpResponseRedirect(reverse("index"))

    list_carreras = Carreras.objects.all()
    return render(request, "tasks/editar.html", {
        "list_carreras":list_carreras,
        "estudiante": estudiante,
    })

@login_required 
def eliminar(request, id):
    estudiante = get_object_or_404(Estudiantes, pk=id)
    estudiante.delete()

    return HttpResponseRedirect(reverse("index"))