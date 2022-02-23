from distutils.command import upload
from enum import unique
from django.conf import settings
from django.db import IntegrityError, models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms.fields import URLField as FormURLField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

def validate_mail(value):
    if "@gmail.com" in value:
        return value
    elif "@hotmail.com" in value:
        return value
    elif "@deneme.com" in value:
        return value        
    else:
        raise ValidationError("please enter hotmail or gmail or deneme.")  

def publish_validate(value):
    if value<timezone.now:
        raise ValueError("Publish date can not be past date.")

   
class TrackerMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(TrackerMixin):
    objects = models.Manager()  # default manager
    published = PublishedManager()  ##Sadece publisleri almak istersen ya bu metodu objectste çağırırsın ya da böyle bırakıp views kısmında Post.objects.all yerine Post.published.all yazarsın.
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish",)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    #content=models.TextField()
    #body=models.TextField()
    #content=RichTextField(default='lorem falan filan')
    #body = RichTextField()
    content=RichTextUploadingField(default='lorem falan filan')
    body =RichTextUploadingField()
    publish = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    image= models.ImageField(blank=True)
    url=models.URLField(max_length=200,default='http://localhost:8000/blog',null=True, blank=True)
    email=models.EmailField(max_length=30,validators =[validate_mail],null=True, blank=True)
    class Meta:
        unique_together=(('title','slug'))

    
    #TODO: *args,**kwargs abstract model
    def get_object_or_None(slug_string):#Bu static olmalı mı acaba? Dışardan kullanmıyorum diye koymadım. Aynı sınıfta olduğu için static yapmadan kullanabilirim bence.
        try:
            obj=Post.objects.get(slug=slug_string)
            return obj
        except ObjectDoesNotExist as e:
            return None

    #TODO en büyüğü döndür direkt sorguda        
    @staticmethod
    def making_slug2(title_string):
        baseslug = slugify(title_string)
        if(Post.get_object_or_None(baseslug) is not None):#metot çağırma gibi işlemleri if'in içinde yapma okunabilirliği azaltıyor. Maliyet artar ama önemsiz.
            slugs_object=Post.objects.filter(slug__startswith=baseslug+"-" , title=title_string)#değişken adı saçma.
            slug_number=2
            for a_object in slugs_object:
                split_slug=a_object.slug.split("-")
                if(int(split_slug[-1])>=slug_number):
                    slug_number=int(split_slug[-1])+1#split'in ikinci halini kullanman lazım değişken isminde ama zaten split
            baseslug=baseslug + "-"+str(slug_number)#değişken adını snake case tarzı ver.
        return baseslug

    #TODO cachelemeye bak.
    @staticmethod
    def making_slug(title_string):
        baseslug = slugify(title_string)
        if(Post.get_object_or_None(baseslug) is not None):
            slug_number=2
            while True:              
                baseslug_temp=baseslug+'-'+str(slug_number)
                if(Post.get_object_or_None(baseslug_temp) is not None):
                    slug_number+=1
                    continue
                else:
                    baseslug=baseslug+'-'+str(slug_number)
                    break
        return baseslug
    

    def save(self, *args, **kwargs):
        #import ipdb;ipdb.set_trace()
        obj_slug = Post.making_slug(self.title)
        self.slug = obj_slug
        super(Post, self).save(*args, **kwargs)
        


'''class slugError(IntegrityError):
    pass'''

