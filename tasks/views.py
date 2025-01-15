from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from . models import Task
from .forms import CreateNewTask
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html' )
def signUp(request):
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })

    else:
        if (request.POST['password1']) != (request.POST['password2']):
            return render(request,'signup.html',{
                'form':UserCreationForm,
                'error':'Password Do not match'
            })
        else:
            try:
                #register user
                user= User.objects.create_user(username=request.POST["username"],password=request.POST['password1'])
                print("obteniendo datos")
                user.save()
                login(request,user)
                user=authenticate(request, username= request.POST['username'], password= request.POST['password1'])

                if user is not None:
                    id = user.id
                    print(id)
                    return redirect('tasks_unico',id)
                

            except IntegrityError:
                return render(request,'signup.html',{
                'form':UserCreationForm,
                'error':'Username already Exists'
                })

@login_required
def tasks(request, id):
    tareas = list(Task.objects.filter(user_id=id))
    if tareas == []:
        print("No hay tareas creadas")
    if request.method == 'GET':
        return render(request, 'tasks.html',{
            'tareas':tareas,
            'createtask':CreateNewTask()
        })
    else:
        try:
            important = request.POST.get('important') == 'on'
            Task.objects.create(tittle=request.POST['tittle'],description= request.POST['description'], created=timezone.now(), important=important, user_id = id )
            return redirect('tasks_unico',id)
        except ValueError:
            return render(request, 'tasks.html',{
                'tareas':tareas,
                'error':'please Plovide valida data'
            })
@login_required
def tasks_completed(request):
    tareas = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'tasks.html',{
        'tareas':tareas
    } )
@login_required
def taskDetails(request, idtask):
    task = get_object_or_404(Task, id=idtask, user=request.user)  # Obtener la tarea o devolver 404 si no existe

    if request.method == 'GET':
        form = CreateNewTask(initial={
            'tittle': task.tittle,
            'description': task.description,
            'important': task.important
        })
        return render(request, 'task_details.html', {'form': form, 'task': task})

    elif request.method == 'POST':
        form = CreateNewTask(request.POST)
        if form.is_valid():
            # Actualiza manualmente los campos del objeto existente
            task.tittle = form.cleaned_data['tittle']
            task.description = form.cleaned_data['description']
            task.important = form.cleaned_data['important']
            task.save()  # Guarda los cambios en la base de datos
            return redirect('tasks_unico',task.user_id)
        else:
            return render(request, 'task_details.html', {'form': form, 'task': task, 'error': 'Datos inválidos'})
@login_required
def taskcomplete(request,idtask):
    task = get_object_or_404(Task, id=idtask, user=request.user)
    task.datecompleted=timezone.now()
    task.save()
    return redirect('tasks_unico', task.user_id)
@login_required
def taskdelete(request, idtask):
    task = get_object_or_404(Task, id= idtask, user= request.user)
    id_user = task.user_id
    task.delete()
    return redirect('tasks_unico',id_user )

def signout(request):
    logout(request)
    return redirect('home')
        
def signin(request):
    if request.method== 'GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else:
        print(request.POST)
        user=authenticate(request, username= request.POST['username'], password= request.POST['password'])

        if user is None:
            return render(request, 'signin.html',{
                'form':AuthenticationForm,
                'error':'Username or password incorrect'
            })
        else:
            login(request,user)
            id = user.id
            print(id)
            return redirect('tasks_unico', id)
                    



