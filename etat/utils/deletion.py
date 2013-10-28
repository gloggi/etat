from django.contrib.admin.util import NestedObjects
from django.utils.encoding import force_text


def deletion_tree(obj):
    ''' Return a list of all nested objects that will be deleted '''
    collector = NestedObjects(using=obj._state.db)
    collector.collect([obj])
    def format_callback(obj):
        return u'%s: %s' % (force_text(obj._meta.verbose_name), force_text(obj))
    return collector.nested(format_callback)
