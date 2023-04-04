import uuid

from collections import OrderedDict
from guardian.shortcuts import assign_perm
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import smart_str

from rest_framework import serializers, viewsets

from utils.responses import ApiResponse, ResponseType
from utils.messages import Message
from utils.resources import retrieve_resource


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             
        queryset = self.filter_queryset(queryset)  
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):  
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
    
        super(TimestampMixin, self).save(*args, **kwargs)


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class AsymmetricRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        self.serializer_class = kwargs.pop('serializer_class')
        super().__init__()

    def to_representation(self, value):
        return self.serializer_class(value).data

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        return self.serializer_class.Meta.model.objects.all()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])

    def use_pk_only_optimization(self):
        return False

    @classmethod
    def from_serializer(cls, serializer, name=None, args=(), kwargs={}):
        if name is None:
            name = f"{serializer.__class__.name}AsymetricAutoField"

        return type(name, [cls], {"serializer_class": serializer})


class CoreViewSet(viewsets.ViewSet):
    require_auth = []
    resource_class = None
    serializer_class = None
    permissions = {
        "create": None,
        "update": None,
        "retrieve": None,
        "list": None,
        "destroy": None
    }

    def pre_create(self, request, **kwargs):
        return request.data.copy()

    def post_create(self, instance, serializer, request):
        resource_name = instance.__class__.__name__.lower()
        change_resource = f"change_{resource_name}"
        delete_resource = f"delete_{resource_name}"

        assign_perm(change_resource, request.user, instance)
        assign_perm(delete_resource, request.user, instance)

    def create(self, request, **kwargs):
        if 'create' in self.require_auth and not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            ) 

        data = self.pre_create(request, **kwargs)
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return ApiResponse(
                'invalid',
                data={
                    'errors': serializer.errors
                }
            )

        instance = serializer.save()
        self.post_create(instance, serializer, request)

        return ApiResponse(
            ResponseType.CREATED,
            data=serializer.data
        )

    def post_list_filter(self, request, resource_list, **kwargs):
        return resource_list

    def list(self, request, **kwargs):
        if 'list' in self.require_auth and not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )
        
        resource_list = self.resource_class.objects.all()
        resource_list = self.post_list_filter(request, resource_list, **kwargs)

        serializer = self.serializer_class(resource_list, many=True)
        return ApiResponse(ResponseType.RETRIEVED, data=serializer.data)
    
    def set_retrieve_fields(self, *args, **kwargs):
        return kwargs

    def retrieve(self, request, **kwargs):
        if 'retrieve' in self.require_auth and not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        resource_fields = self.set_retrieve_fields(request, **kwargs)
        resource, success = retrieve_resource(self.resource_class, resource_fields)

        if not success:
            return ApiResponse(
                'not-found',
                message=Message.NOT_FOUND.format(self.resource_class, kwargs.pop('pk'))
            )

        serializer = self.serializer_class(resource)

        return ApiResponse(
            'retrieved',
            data=serializer.data
        )

    def pre_update(self, request, resource):
        return request.data.copy()

    def post_update(self, request, serializer):
        pass

    def set_update_fields(self, request, *args, **kwargs):
        return kwargs

    def update(self, request, **kwargs): 
        if 'update' in self.require_auth and not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        resource_fields = self.set_update_fields(request, **kwargs)
        resource, success = retrieve_resource(self.resource_class, resource_fields)

        if not success:
            return ApiResponse(
                'not-found',
                message=Message.NOT_FOUND.format(self.resource_class, kwargs.pop('pk'))
            )

        if 'update' in self.permissions.keys() and not request.user.has_perm(self.permissions['update'], resource):
            return ApiResponse(
                'unauthorized',
                message=Message.NOT_AUTHORIZED
            )

        data = self.pre_update(request, resource)
        serializer = self.serializer_class(resource, data=data, partial=True)

        if not serializer.is_valid():
            return ApiResponse(
                'invalid',
                data={
                    'errors': serializer.errors
                }
            )

        serializer.save()
        self.post_update(request, serializer)

        return ApiResponse(
            'updated',
            data=serializer.data
        )

    def pre_destroy(self, request, resource):
        pass

    def post_destroy(self, request, resource):
        pass

    def set_delete_fields(self, *args, **kwargs):
        return kwargs

    def destroy(self, request, **kwargs):
        if 'destroy' in self.require_auth and not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        resource_fields = self.set_delete_fields(request, **kwargs)
        resource, success = retrieve_resource(self.resource_class, resource_fields)

        if not success:
            return ApiResponse(
                'not-found',
                message=Message.NOT_FOUND.format(self.resource_class, kwargs.pop('pk'))
            )
        
        if 'destroy' in self.permissions.keys() and not request.user.has_perm(self.permissions['destroy'], resource):
            return ApiResponse(
                'unauthorized',
                message=Message.NOT_AUTHORIZED
            )

        self.pre_destroy(request, resource)
        resource.delete()
        self.post_destroy(request, resource)

        return ApiResponse(ResponseType.DESTROYED)
