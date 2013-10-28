from django.db.models import Q
from django.utils.timezone import now

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import BaseFilterBackend
from rest_framework.serializers import ModelSerializer, RelatedField

import models


class MemberFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        filter_args = []
        departments = request.GET.getlist('departments[]')
        roles = request.GET.getlist('roles[]')
        education = request.GET.getlist('education[]')
        status = request.GET.get('status')
        gender = request.GET.get('gender')

        if departments:
            filter_args.append(Q(departments__id__in=departments))

        if roles:
            filter_args.append(Q(roles__type__id__in=roles))

        if education:
            filter_args.append(Q(educations__type__id__in=education))

        if gender:
            filter_args.append(Q(gender=gender))

        if status == 'active':
            filter_args.append(
                Q(roles__end__isnull=True) |
                Q(roles__end__gte=now())
            )
        elif status == 'inactive':
            filter_args.append(Q(roles__end__lte=now()))
        elif status == 'none':
            return queryset.none()

        return queryset.filter(*filter_args).distinct()


class RoleInlineSerializer(ModelSerializer):
    type = RelatedField(read_only=True)

    class Meta:
        model = models.Role
        fields = ('department', 'type')

    def to_native(self, obj):
        data = super(RoleInlineSerializer, self).to_native(obj)
        data['active'] = obj.active
        return data


class MemberSerializer(ModelSerializer):
    roles = RoleInlineSerializer(many=True)

    class Meta:
        model = models.Member


class MemberViewSet(ModelViewSet):
    model = models.Member
    filter_backends = (MemberFilter,)
    serializer_class = MemberSerializer


class RoleTypeViewSet(ModelViewSet):
    model = models.RoleType


class RoleViewSet(ModelViewSet):
    model = models.Role


class AddressViewSet(ModelViewSet):
    model = models.Address


class ReachabilityViewSet(ModelViewSet):
    model = models.Reachability
