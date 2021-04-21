from django.db import models

from users.models import User


class GeneralInformation(models.Model):
    name = models.CharField('Имя парикмахерской', max_length=15)
    main_photo = models.ImageField('Главное фото', upload_to='main_photo/')
    attainment_photo = models.ImageField('Фото с достижениям', upload_to='attainment_photo/')
    contact_number = models.CharField('Номер для связи', max_length=14)
    contact_email = models.EmailField()
    location = models.CharField('Расположение парикмахерской', max_length=50)
    working_days = models.CharField('Рабочие дни', max_length=30)
    working_hours = models.CharField('Рабочие часы', max_length=10)
    description = models.TextField('Описание парикмахерской', max_length=1000)
    mini_text = models.CharField('Краткое описание парикмахерской', max_length=255)


class Specialization(models.Model):
    name = models.CharField('Имя специализации', max_length=25)
    about = models.CharField('О специализации', max_length=255)


class Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialisation = models.ManyToManyField(Specialization, verbose_name='Специализации')
    photo = models.ImageField('Фото мастера', upload_to='master/')
    about = models.CharField('Немного о себе', max_length=255)

    def __str__(self):
        return f'Мастер {self.user.get_full_name()}'


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


class ServicePrice(models.Model):
    name = models.CharField('Название улуги', max_length=40)
    price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)


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
