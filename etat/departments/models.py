from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class DepartmentType(models.Model):

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Department type')
        verbose_name_plural = _('Department types')

    def __unicode__(self):
        return self.name


class Department(MPTTModel):

    name = models.CharField(_('name'), max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')
    type = models.ForeignKey(DepartmentType, blank=True, null=True)
    default_role = models.ForeignKey('members.RoleType', null=True, blank=True,
        verbose_name=_('default role'), related_name='+')

    notes = models.TextField(_('notes'), blank=True)
    website = models.URLField(_('website'), null=True, blank=True)
    logo = models.ImageField(_('logo'), upload_to='departments',
        null=True, blank=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Department, self).save(*args, **kwargs)
        Department.objects.rebuild()