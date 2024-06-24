# hotel_app/models.py

from django.db import models
from django.contrib import admin
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User

class Blog(models.Model):

    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")

    description = models.TextField(verbose_name = "Краткое содержание")

    content = models.TextField(verbose_name = "Полное содержание")

    posted = models.DateTimeField(default = datetime.utcnow(), db_index = True, verbose_name = "Опубликована")
    author=models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name ="Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    
    # Методы класса:

    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
            return self.title

    # Метаданные – вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ['-posted'] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    agree_to_news = models.BooleanField(default=False)  # Новое поле для согласия на получение новостей

    def __str__(self):
        return self.name


from django.db import models

class Anketa(models.Model):
    second_name = models.CharField(max_length=100, verbose_name='Фамилия')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    RESERVATION_CHOICES = (
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )

    reservation = models.CharField(
        verbose_name='Насколько быстро и просто вы забронировали номер?',
        choices=RESERVATION_CHOICES,
        max_length=1,
        default='5'  # Установка значения по умолчанию на '5'
    )
    city = models.CharField(max_length=100, verbose_name='Ваш город')
    job = models.CharField(max_length=100, verbose_name='Ваш род занятий')
    work = models.CharField(
        max_length=1,
        choices=(('5','5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')),
        default='5',
        verbose_name='Оцените качество работы персонала'
    )
    back = models.CharField(max_length=1, choices=(('1','Да'), ('2', 'Нет')), verbose_name='Хотели бы вы приехать к нам еще?')
    email = models.EmailField(verbose_name='Ваш e-mail')
    message = models.TextField(verbose_name='Отзыв')
    notice = models.BooleanField(default=False, verbose_name='Хочу получать новости на электронную почту')

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

class Comment(models.Model):
    text=models.TextField(verbose_name="текст комментария")
    date=models.DateTimeField(default=datetime.now(),db_index=True, verbose_name="Дата комментария")
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post=models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")
    #Методы
    def __str__(self):
        return 'Комментарий %d %s k %s' % (self.id, self.author, self.post)
    
    #Вложенный класс который задает дополнительные параметры
    class Meta:
        db_table="Comment"
        ordering=["-date"]
        verbose_name="Комментарии к статье блога"
        verbose_name_plural="Комментарии к статье блога"
admin.site.register(Comment)