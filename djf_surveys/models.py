import random, string
from collections import namedtuple

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.safestring import mark_safe

from djf_surveys import app_settings
from djf_surveys.utils import create_star


TYPE_FIELD = namedtuple(
    'TYPE_FIELD', 'text number radio select multi_select text_area url email date rating'
)._make(range(10))


def generate_unique_slug(klass, field, id):
    """
    generate unique slug.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    obj = klass.objects.filter(slug=unique_slug).first()
    while obj:
        if obj.id == id:
            break
        rnd_string = random.choices(string.ascii_lowercase, k=(len(unique_slug)))
        unique_slug = '%s-%s-%d' % (origin_slug, ''.join(rnd_string[:10]), numb)
        numb += 1
        obj = klass.objects.filter(slug=unique_slug).first()
    return unique_slug


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Survey(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    slug = models.SlugField(max_length=225, default='')
    editable = models.BooleanField(default=True, help_text="if False, user can't edit record")
    deletable = models.BooleanField(default=True, help_text="if False, user can't delete record")
    duplicate_entry = models.BooleanField(default=False, help_text="if True, user can resubmit")
    private_response = models.BooleanField(default=False, help_text="if True, admin and owner can access")
    can_anonymous_user = models.BooleanField(default=False, help_text="if True, user without auth can submit")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = generate_unique_slug(Survey, self.slug, self.id)
        else:
            self.slug = generate_unique_slug(Survey, self.name, self.id)
        super().save(*args, **kwargs)


class Question(BaseModel):
    TYPE_FIELD = [
        (TYPE_FIELD.text, "Text"),
        (TYPE_FIELD.number, "Number"),
        (TYPE_FIELD.radio, "Radio"),
        (TYPE_FIELD.select, "Select"),
        (TYPE_FIELD.multi_select, "Multi Select"),
        (TYPE_FIELD.text_area, "Text Area"),
        (TYPE_FIELD.url, "URL"),
        (TYPE_FIELD.email, "Email"),
        (TYPE_FIELD.date, "Date"),
        (TYPE_FIELD.rating, "Rating")
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    label = models.CharField(max_length=200, help_text='Enter your question in here')
    type_field = models.PositiveSmallIntegerField(choices=TYPE_FIELD)
    choices = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='if Type Field is (radio, select, multi select), fill in the option separated by commas. ex: Male, Female'
    )
    help_text = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='You can add a help text in here'
    )
    required = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.survey.name


class UserAnswer(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.id)

    def get_user_photo(self):
        if app_settings.SURVEY_USER_PHOTO_PROFILE:
            return eval(app_settings.SURVEY_USER_PHOTO_PROFILE)
        return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    value = models.TextField()
    user_answer = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question}: {self.value}'

    @property
    def get_value(self):
        if self.question.type_field == TYPE_FIELD.rating:
            return create_star(active_star=int(self.value))
        elif self.question.type_field == TYPE_FIELD.url:
            return mark_safe(f'<a href="{self.value}" target="_blank">{self.value}</a>')
        else:
            return self.value
