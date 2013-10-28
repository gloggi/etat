from django import template

register = template.Library()

@register.inclusion_tag('partials/_form_header.html')
def form_header(form):
    return {'form': form}

@register.inclusion_tag('partials/_formset_errors.html')
def formset_errors(formset):
    return {'formset': formset}

@register.inclusion_tag('partials/_formset_table_rows.html')
def formset_table_rows(formset):
    return {'formset': formset}

@register.inclusion_tag('partials/_formset_table_row.html')
def formset_table_row(form):
    return {'form': form}