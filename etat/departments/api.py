from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response

import models


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = models.Department
        exclude = ('lft', 'rght', 'level', 'tree_id')

    def to_native(self, obj):
        data = super(DepartmentSerializer, self).to_native(obj)
        data['label'] = data.get('name')
        return data


class DepartmentViewSet(ModelViewSet):
    model = models.Department
    serializer_class = DepartmentSerializer

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset().filter(level=0)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        self.object = self.get_object()
        data = self.serialize_tree([self.object])
        return Response(data)

class DepartmentTypeViewSet(ModelViewSet):
    model = models.DepartmentType


# @api_view(['GET'])
# def department_tree(request):
#     return Response({"message": "Hello, world!"})
