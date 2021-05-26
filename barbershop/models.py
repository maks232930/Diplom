from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class GeneralInformation(models.Model):
    name = models.CharField('Имя парикмахерской', max_length=15)
    heading = models.CharField('Слоган', max_length=50)
    main_photo = models.ImageField('Главное фото', upload_to='main_photo/')
    attainment_photo = models.ImageField('Фото с достижениям', upload_to='attainment_photo/')
    contact_number = models.CharField('Номер для связи', max_length=20)
    contact_number_description = models.CharField('Примечание к номеру', max_length=50, blank=True)
    contact_email = models.EmailField()
    location = models.CharField('Расположение парикмахерской', max_length=50)
    location_description = models.CharField('Примечание к расположению', max_length=50, blank=True)
    working_days = models.CharField('Рабочие дни', max_length=30)
    working_hours = models.CharField('Рабочие часы', max_length=20)
    description = models.TextField('Описание парикмахерской', max_length=1000)
    mini_text = models.CharField('Краткое описание парикмахерской', max_length=255)

    def __str__(self):
        return 'Общая информация'

    class Meta:
        verbose_name = 'Общая информация'
        verbose_name_plural = 'Общая информация'


class Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialisation = models.CharField('Специализация', max_length=50)
    services = models.ManyToManyField('Service', verbose_name='Выберите предостовляемые услуги')
    photo = models.ImageField('Фото мастера', upload_to='master/')
    about = models.TextField('Немного о себе', max_length=300)

    def __str__(self):
        return f'Мастер {self.user.get_full_name()}'

    def get_services(self):
        return self.services.all()

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class SocialLink(models.Model):
    SOCIAL_LINK = [
        ('vk', 'Vk'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('dribbble', 'Dribbble'),
        ('amazon', 'Amazon'),
        ('github', 'Github'),
        ('instagram', 'Instagram'),
        ('skype', 'Skype'),
        ('youtube-1', 'Youtube'),
        ('linkedin', 'Linkedin')
    ]
    name = models.CharField(verbose_name='Имя соцсети', choices=SOCIAL_LINK, max_length=15)
    link = models.URLField('Ссылка на соцсеть')

    def __str__(self):
        return f'{self.name} {self.link}'

    class Meta:
        verbose_name = "Соцсеть"
        verbose_name_plural = "Соцсети"


class Specialization(models.Model):
    name = models.CharField('Название категории услуг', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'


class Gallery(models.Model):
    photo = models.ImageField('Фото для галереи', upload_to='gallery/')

    def __str__(self):
        return 'Фото'

    class Meta:
        verbose_name = 'Фото для галереи'
        verbose_name_plural = 'Фото для галереи'


class Service(models.Model):
    specialisation = models.ForeignKey(Specialization, verbose_name='Категория услуг', on_delete=models.CASCADE)
    name = models.CharField('Название улуги', max_length=100)
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)
    execution_time = models.PositiveIntegerField('Время выполнения(в минутах)')
    about = models.CharField('О услуге', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Категория: {self.specialisation.name}. Название: {self.name}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Message(models.Model):
    first_name = models.CharField('Ваше имя', max_length=30)
    email = models.EmailField(verbose_name='Ваш email', max_length=100)
    subject = models.CharField('Тема', max_length=20)
    message = models.TextField('Сообщение', max_length=5000)

    def __str__(self):
        return f'Сообщение от {self.first_name}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщение'


class Statistics(models.Model):
    name = models.CharField('Имя достижения', max_length=50)
    count = models.PositiveIntegerField('Количество')

    def __str__(self):
        return f'Достижение {self.name} в количестве {self.count}'

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Recording(models.Model):
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    date_and_time_of_recording = models.ManyToManyField('FreeTime', verbose_name='Время записи')
    phone = PhoneNumberField()
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)
    date_time = models.DateTimeField('Дата и время', auto_now_add=True)

    def __str__(self):
        return f'Заказ на {self.date_and_time_of_recording}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class FreeTime(models.Model):
    """Свободное время"""
    STATUSES = [
        ('start_day', 'Начало дня'),
        ('end_day', 'Конец дня'),
        ('works_free', 'Работает, свободен'),
        ('works_busy', 'Работает, занят'),
        ('does_not_work', 'Не работает'),
    ]

    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')
    date_time = models.DateTimeField('Дата и время', default=timezone.now)
    status = models.CharField('Статус', choices=STATUSES, max_length=15, default='works_free')

    def __str__(self):
        return f'Мастер: {self.master.user.get_full_name()}. Время: {self.date_time}'

    class Meta:
        verbose_name = 'Свободное время'
        verbose_name_plural = 'Свободное время'
        ordering = ('-date_time',)


class Review(models.Model):
    """Модель отзывов"""
    name = models.CharField('ФИО', max_length=100)
    email = models.EmailField('Email')
    message = models.TextField('Сообщение', max_length=9999999)
    is_show = models.BooleanField('Показывать?', default=True)
    date_time = models.DateTimeField('Дата и время', auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.name}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class TwilioSettings(models.Model):
    account_sid = models.CharField('ACCOUNT SID', max_length=255)
    auth_token = models.CharField('AUTH TOKEN', max_length=255)
    phone_number = models.CharField('PHONE NUMBER', max_length=25)

    def __str__(self):
        return f'Номер {self.phone_number}'

    class Meta:
        verbose_name = 'Телефон для оповещения'
        verbose_name_plural = 'Телефоны для оповещения'
