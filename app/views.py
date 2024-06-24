from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import  BlogForm, FeedbackForm
from .forms import AnketaForm
from .forms import CommentForm # использование формы ввода комментария
from .models import Comment # использование модели комментариев
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.db import models, connection


def blog(request):

    # posts = Blog.objects.all() # ORM
    
    posts=Blog.objects.raw("SELECT * FROM Posts") #Выбор всех постов с использованием SQL
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/blog.html',
        {
            'title':'Новости',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
    
def edit_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # form.save()  # Сохранение данных формы в базе данных
            # return redirect('blogpost', parametr=post_id)  # Перенаправление на страницу поста после редактирования

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            # Получаем имя файла, если есть
            if 'image' in form.cleaned_data and form.cleaned_data['image']:
                image = form.cleaned_data['image'].name
            else:
                image = post.image.name  # или post.image, в зависимости от структуры модели
            

            # Обовление данных с использованием SQL-запроса
            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE Posts SET title = %s, content = %s, image = %s WHERE id = %s """, [title, content, image, post_id])

            return redirect('blogpost', parametr=post_id)  # Перенаправление на страницу поста после редактирования

    else:
        form = BlogForm(instance=post)
    
    return render(request, 'app/edit_post.html', {
        'form': form,
        'post': post
    })


def delete_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id, author=request.user)
    if request.method == "POST":
       post.delete()   # Удаление постаа с использованием ORM
       # Выполнение SQL запроса для удаления данных
        # with connection.cursor() as cursor:
        #     cursor.execute("DELETE FROM Posts WHERE id = %s", [post_id])
    return redirect('blog')

def blogpost(request, parametr):
    assert isinstance(request, HttpRequest)
    #post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    post_1 = Blog.objects.raw("SELECT * FROM Posts WHERE id = %s", [parametr])
    
    # Проверяем, что пост существует
    if not post_1:
        post_1 = None
    else:
        post_1 = post_1[0]  # Получаем первый (и единственный) результат
    
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария


    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }

    )
    


def registration(request):
    if request.method=="POST":
        regform=UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f=regform.save(commit=False)
            reg_f.is_staff=False
            reg_f.is_active=True
            reg_f.is_superuser=False
            reg_f.date_joined=datetime.now()
            reg_f.last_login=datetime.now()
        regform.save()
        
        return redirect('home')
    else:
        regform=UserCreationForm()
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform':regform,
            'year':datetime.now().year,
        }
    )
    
def home(request):
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/index.html',
       { 'title':'Главная',
        'year': datetime.now().year,}
    )
    

def anketa_view(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['second_name'] = form.cleaned_data['second_name']
            data['first_name'] = form.cleaned_data['first_name']
            data['reservation'] = form.cleaned_data['reservation']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['work'] = form.cleaned_data['work']
            data['back'] = form.cleaned_data['back']
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            data['notice'] = form.cleaned_data['notice']
            
            # Сохраняем данные в базе данных или другом хранилище

            return render(request, 'app/anketa.html', {'form': form, 'data': data})

    else:
        form = AnketaForm()

    return render(request, 'app/anketa.html', {'form': form})



def layout_view(request):
    return render(request, 'app/layout.html', {})
def index(request):
    return render(request, 'app/index.html')
def rooms(request):
    return render(request, 'app/rooms.html')
def add(request):
    return render(request, 'app/add.html')
def contacts(request):
    return render(request, 'app/contacts.html')
def feedback(request):
    return render(request, 'app/feedback.html')
def about(request):
    return render(request, 'app/about.html')
def add(request):
    return render(request, 'app/add.html')
def booking(request):
    return render(request, 'app/booking.html')
def videopost(request):
    return render(request, 'app/videopost.html')
def kino(request):
    return render(request, 'app/kino.html')
def parking(request):
    return render(request, 'app/parking.html')
def standart(request):
    return render(request, 'app/rooms/standart.html')
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Возвращаем JSON об успешной отправке
        else:
            # Если форма не валидна, возвращаем ошибки валидации в JSON
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = FeedbackForm()
    return render(request, 'app/feedback.html', {'form': form})
def newpost(request):
    assert isinstance(request,HttpRequest)
    if request.method=="POST":
        blogform=BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            # blog_f=blogform.save(commit=False)
            # blog_f.posted=datetime.now()
            # blog_f.author=request.user
            # blog_f.save()
            # newblog=Blog.objects.create( #ORM
            #     title=blogform.cleaned_data['title'],
            #     content=blogform.cleaned_data['content'],
            #     image=blogform.cleaned_data['image'],
            #     posted=datetime.now(),
            #     author=request.user,)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Posts (title, description, content, image, posted, author_id) VALUES (%s, %s, %s, %s, %s, %s)", 
                [blogform.cleaned_data['title'], blogform.cleaned_data['description'], blogform.cleaned_data['content'], blogform.cleaned_data['image'], 
                datetime.now(), request.user.id])
                newblog=Blog.objects.get(title=blogform.cleaned_data['title'])
                return redirect('blog')
            return redirect('blog')
    else:
        blogform=BlogForm()
    return render(
            request,
            'app/newpost.html',
            {
                'blogform': blogform,
                'title': 'Добавить статью блога',
                'year':datetime.utcnow().year,
            }
        )




            