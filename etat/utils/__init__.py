
from mptt.forms import TreeNodeChoiceFieldMixin
from django.utils.safestring import mark_safe
# Monkey patch default mptt level indicator

def init_other_indicator(self, queryset, *args, **kwargs):
    self.level_indicator = kwargs.pop('level_indicator', mark_safe('&ensp;'))
    # if a queryset is supplied, enforce ordering
    if hasattr(queryset, 'model'):
        mptt_opts = queryset.model._mptt_meta
        queryset = queryset.order_by(mptt_opts.tree_id_attr, mptt_opts.left_attr)
    super(TreeNodeChoiceFieldMixin, self).__init__(queryset, *args, **kwargs)


TreeNodeChoiceFieldMixin.__init__ = init_other_indicator
