from django import forms
from django.utils.safestring import mark_safe
from sorl.thumbnail.shortcuts import get_thumbnail

from django_select2.widgets import Select2Widget

class ImageWidget(forms.ClearableFileInput):
    template_with_initial = u'%(clear_template)s<br />%(input_text)s: %(input)s'
    template_with_clear = u'%(clear)s <label style="width:auto" for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None):
        output = super(ImageWidget, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            try:
                mini = get_thumbnail(value, '172x172', upscale=False)
            except Exception:
                pass
            else:
                output = u'<div class="portrait clearfix"><img src="%s">%s</div>' % (mini.url, output)
        return mark_safe(output)


class SuitSelect(Select2Widget):

    def __init__(self, *args, **kwargs):
        self.options['width'] = '220px'
        super(SuitSelect, self).__init__(*args, **kwargs)
