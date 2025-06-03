from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

class BaseRepository:
    model = None

    @classmethod
    def get(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def create(cls, **kwargs):
        with transaction.atomic():
            return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def all(cls):
        return cls.model.objects.all()
