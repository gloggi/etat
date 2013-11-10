
from rest_framework.viewsets import ModelViewSet

import models

class MemberViewSet(ModelViewSet):
    queryset = models.Member.objects.all().prefetch_related('departments')

class RoleTypeViewSet(ModelViewSet):
    model = models.RoleType


class RoleViewSet(ModelViewSet):
    model = models.Role


class AddressViewSet(ModelViewSet):
    model = models.Address


class ReachabilityViewSet(ModelViewSet):
    model = models.Reachability
