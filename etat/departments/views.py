
import json

from django.http import HttpResponse

from .models import Department

from mptt.templatetags.mptt_tags import cache_tree_children


def serialize_tree(queryset):
    data = []
    for obj in queryset:
        dep = {
            'id': obj.id,
            'label': obj.name,
        }
        if obj._cached_children:
            dep['children'] = serialize_tree(obj._cached_children)
        data.append(dep)
    return data


def department_data(request):
    departments = Department.objects.filter(active=True)
    tree = cache_tree_children(departments)
    data = serialize_tree(tree)
    return HttpResponse(json.dumps(data), mimetype="application/json")