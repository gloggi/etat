from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from mptt.fields import TreeForeignKey
from django_countries import CountryField

from sorl.thumbnail import ImageField

from etat.commons import STEPS
from etat.departments.models import Department


class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    legacy_id = models.PositiveIntegerField(blank=True, null=True,
        editable=False, unique=True)

    class Meta:
        abstract = True


class Member(BaseModel):
    GENDER_CHOICES = (
        ('f', _('female')),
        ('m', _('male')),
    )

    scout_name = models.CharField(_('scout name'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    portrait = ImageField(_('portrait'), null=True, blank=True,
        upload_to='members')
    gender = models.CharField(_('gender'), max_length=2, choices=GENDER_CHOICES,
        default='m')
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    application = models.BooleanField(_('application'), default=False)

    departments = models.ManyToManyField('departments.Department',
        through='Role', related_name='members')

    user = models.OneToOneField(User, blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')

    def __unicode__(self):
        return self.fullname

    @property
    def fullname(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def address(self):
        try:
            return self.addresses.get(main=True)
        except:
            return None

    def editable_departments(self):
        department_ids = set()

        for department in self.departments.all():
            descendants = department.get_descendants(include_self=True)
            for descendant in descendants:
                department_ids.add(descendant.id)

        return Department.objects.filter(id__in=department_ids)


class RoleType(BaseModel):

    name = models.CharField(_('name'), max_length=100)
    step = models.IntegerField(_('step'), choices=STEPS, blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Role type')
        verbose_name_plural = _('Role types')
        ordering = ('order',)

    def __unicode__(self):
        return self.name


class RoleManager(models.Manager):

    def active(self):
        return self.filter(Q(end__isnull=True) | Q(end__gte=now()))

    def inactive(self):
        return self.filter(end__lte=now())


class Role(BaseModel):
    member = models.ForeignKey(Member, related_name='roles')
    department = TreeForeignKey('departments.Department', related_name='roles')
    type = models.ForeignKey(RoleType, related_name='roles')

    start = models.DateField(_('start'), null=True, blank=True)
    end = models.DateField(_('end'), null=True, blank=True)

    # Daily calculated for speed improvement
    active = models.BooleanField(editable=False)

    objects = RoleManager()

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def clean(self):
        if self.start and self.end and self.start >= self.end:
            raise ValidationError(_('Start data has to be before end date!'))

    def __unicode__(self):
        return _('%(type)s at %(department)s') % {
            'type': self.type,
            'department': self.department
        }

    def save(self, *args, **kwargs):
        self.active = not self.end or self.end >= now().date()
        super(Role, self).save(*args, **kwargs)


class Address(BaseModel):

    member = models.ForeignKey(Member, related_name='addresses')

    street = models.CharField(_('street'), max_length=100)
    postal_code = models.PositiveIntegerField(_('post code'))
    city = models.CharField(_('city'), max_length=100)
    country = CountryField(_('country'), default='CH')
    main = models.BooleanField(_('main address'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def save(self, *args, **kwargs):
        if self.main:
            my_id = getattr(self, 'id', None)
            self.member.addresses.exclude(pk=my_id).update(main=False)
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s, %s %s' % (self.street, self.postal_code, self.city)

class Reachability(BaseModel):

    TYPE_CHOICES = (
        ('email',       _('Email')),
        ('phone',      _('Phone')),
        ('skype',       _('Skype')),
        ('facebook',    _('Facebook')),
        ('twitter',     _('Twitter')),
    )

    KIND_CHOICES = (
        ('private', _('Private')),
        ('work',    _('Work')),
        ('scout',   _('Scout')),
        ('other',   _('Other')),
    )

    member = models.ForeignKey(Member, related_name='reachabilities')

    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    kind = models.CharField(_('kind'), max_length=20, choices=KIND_CHOICES,
        blank=True)

    value = models.CharField(_('value'), max_length=100)

    class Meta:
        verbose_name = _('Reachability')
        verbose_name_plural = _('Reachabilities')

    def __unicode__(self):
        return u'%s %s' % (self.type, self.value)

    icons = {
        'email': 'fa fa-envelope',
        'phone': 'fa fa-phone',
        'skype': 'fa fa-skype',
        'facebook': 'fa fa-facebook',
        'twitter': 'fa fa-twitter',
    }

    def icon_class(self):
        return self.icons.get(self.type)


class EducationType(BaseModel):
    title = models.CharField(_('title'), max_length=100)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Education type')
        verbose_name_plural = _('Education types')
        ordering = ('order',)

    def __unicode__(self):
        return self.title


class Education(BaseModel):
    member = models.ForeignKey(Member, related_name='educations')
    type = models.ForeignKey(EducationType)

    date = models.DateField(_('date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')

    def __unicode__(self):
        return self.type.title
