from django.db import models

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


class Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialisation = models.CharField('Специализация', max_length=50)
    service = models.ManyToManyField('Service', verbose_name='услуги')
    photo = models.ImageField('Фото мастера', upload_to='master/')
    about = models.CharField('Немного о себе', max_length=255)

    def __str__(self):
        return f'Мастер {self.user.get_full_name()}'


class WorkingHours(models.Model):
    DAYS_OF_WEEKS = [
        ('пн', 'Понедельник'),
        ('вт', 'Вторник'),
        ('ср', 'Среда'),
        ('чт', 'Четвер'),
        ('пт', 'Пятница'),
        ('сб', 'Субота'),
        ('вс', 'Воскресенье'),
    ]

    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')
    day_of_week = models.CharField('День недели', choices=DAYS_OF_WEEKS, max_length=10)
    is_working = models.BooleanField('Работает?', default=True)
    start_working = models.TimeField('Начало работы', null=True)
    end_working = models.TimeField('Конец работы', null=True)
    start_break = models.TimeField('Начало перерыва', null=True)
    end_break = models.TimeField('Конец перерыва', null=True)


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


class Gallery(models.Model):
    photo = models.ImageField('Фото для галереи', upload_to='gallery/')


class Service(models.Model):
    name = models.CharField('Название улуги', max_length=40)
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)
    execution_time = models.TimeField('Время выполнения')
    about = models.CharField('О услуге', max_length=100, blank=True, null=True)


class Message(models.Model):
    first_name = models.CharField('Ваше имя', max_length=30)
    email = models.EmailField(verbose_name='Ваш email', max_length=100)
    subject = models.CharField('Тема', max_length=20)
    message = models.TextField('Сообщение', max_length=5000)


class Statistics(models.Model):
    name = models.CharField('Имя достижения', max_length=15)
    count = models.PositiveIntegerField('Количество')

    def __str__(self):
        return f'Достижение {self.name} в количестве {self.count}'

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class Recording(models.Model):
    master = models.ForeignKey(Master, on_delete=models.SET_DEFAULT, default='Уже не работает')
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    date_and_time_of_recording = models.DateTimeField('Дата и врямя записи')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default='007',
        verbose_name='Клиент',
        blank=True,
        null=True)
    phone = models.CharField('Телефон для связи', max_length=20, blank=True, null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)
