from django.core.exceptions import ObjectDoesNotExist
def get_object_or_None(klass,*args,**kwargs):
    try:
        if hasattr(klass, '_default_manager'):
            klass=klass._default_manager.all()
        obj=klass.get(*args,**kwargs)
        return obj
    except ObjectDoesNotExist as e:
        return None
