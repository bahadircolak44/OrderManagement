from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from OrderManagement import config
from api import models
from api.serializers import GenericModelSerializer, OrderCompleteSerializers
from utils.viewset import GenericViewSet


class ApiViewSet(GenericViewSet):
    """
    Don't need to write viewset for all api, if all of them are running for the same actions:
        - Create
        - List
        - Retrieve
    """

    serializer_class = GenericModelSerializer

    def __init__(self, *args, **kwargs):
        basename = kwargs.get('basename')
        attribute = config.__dict__.get(basename.upper())
        db_model = getattr(models, attribute.get('db'))
        self.db_model = db_model
        self.attribute = attribute
        self.basename = basename
        self.queryset = db_model.objects.all()
        self.pagination_class = None

        super().__init__(**kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_created = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if is_created:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response('Restaurant is not available.', status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        """
        To use GenericSerializer, we need correct data to be provided.
        Thus, we need to overwrite get_serializer func.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        fields = self.attribute.get('FIELD_LIST')
        read_only_fields = self.attribute.get('READ_ONLY_FIELD_LIST')
        extra_fields = self.attribute.get('EXTRA_FIELDS')
        return serializer_class(model=self.db_model, fields=fields, read_only_fields=read_only_fields,
                                extra_fields=extra_fields, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Later, another models need to publish message, so I made it generic. If you want to use pubsub mechani
        it should publish into redis, it will be consumed later
        """
        serializer.save()
        return self.db_model.publish_message(serializer, basename=self.basename, user_id=self.request.user.id)

    @action(methods=['GET'], detail=False, url_path='list_by_user', url_name='list_by_user')
    def list_by_user(self, request, *args, **kwargs):
        """
        If consume endpoint wanted, need to be defined in Model, otherwise it will return 404.
        """
        return self.db_model.list_by_user(self.get_serializer, self.request.user.id)

    @action(methods=['POST'], detail=False, url_path='complete', url_name='complete')
    def complete(self, request, *args, **kwargs):
        """
        If complete endpoint wanted, need to be defined in Model, otherwise it will return 404.
        This endpoint will change order status from RUNNING to SUCCESS
        """
        return self.db_model.complete(OrderCompleteSerializers, self.request.data)

    @action(methods=['POST'], detail=False, url_path='generate_test_data', url_name='generate_test_data')
    def generate_test_data(self, request, *args, **kwargs):
        """
        If complete endpoint wanted, need to be defined in Model, otherwise it will return 404.
        This endpoint will change order status from RUNNING to SUCCESS
        """
        # if settings.DEBUG:
        from api.models import Category, Food, Restaurant
        if Category.objects.all().count() == 0:
            Category.generate_initial()
        if Restaurant.objects.all().count() == 0:
            Restaurant.generate_initial()
        if Food.objects.all().count() == 0:
            Food.generate_initial()
        return Response(status=status.HTTP_201_CREATED)
