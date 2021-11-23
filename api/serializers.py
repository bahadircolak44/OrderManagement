from rest_framework import serializers


class GenericModelSerializer(serializers.ModelSerializer):
    """
    This serializer is very useful and generic serializer so that you do not have to define multiple serializer for each models.
    Model, fields, exclude or even extra_fields can be send as a parameter.
    """

    def __init__(self, *args, **kwargs):
        # for re-usability
        self.Meta.fields = None
        self.Meta.exclude = None
        self.many = kwargs.pop('many', False)
        extra_fields = kwargs.pop('extra_fields', None)  # If you need more fields other than model
        model = kwargs.pop('model', None)
        fields = kwargs.pop('fields', None)
        read_only_fields = kwargs.pop('read_only_fields', None)
        exclude = kwargs.pop('exclude', None)
        if fields:
            self.Meta.fields = fields
        elif exclude:
            self.Meta.exclude = exclude
        if model:
            self.Meta.model = model
        if read_only_fields:
            self.Meta.read_only_fields = read_only_fields
        if extra_fields:
            for _field, _value in extra_fields.items():
                self.fields[_field] = _value
        super().__init__(*args, **kwargs)

    class Meta:
        pass


class OrderCompleteSerializers(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField(required=True, allow_null=False)
