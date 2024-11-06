import logging

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

logger = logging.getLogger(__name__)
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f'Пользователь успешно вошел в систему.')
            return redirect('note_list')
    return render(request, 'registration/login.html')
'''def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('note_list')
        else:
            # Handle form errors
            # (e.g., display them in the template)
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})'''

###
def logout_view(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа

def home_view(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)  # Получаем заметки пользователя
        return render(request, 'note_list.html', {'notes': notes})
    return redirect('login')  # Если не авторизован, перенаправляем на вход
###

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)  # Показываем только заметки текущего пользователя
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Устанавливаем текущего пользователя как автора заметки
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Проверяем, что заметка принадлежит пользователю
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Проверяем, что заметка принадлежит пользователю
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

