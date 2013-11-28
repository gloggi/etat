from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey

from etat.base import BaseModel


class CampType(BaseModel):
    title = models.CharField(_('title'), max_length=100)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Camp type')
        verbose_name_plural = _('Camp types')
        ordering = ('order',)

    def __unicode__(self):
        return self.title


class Camp(BaseModel):
    title = models.CharField(_('title'), max_length=100)
    type = models.ForeignKey(CampType, blank=True, null=True)
    department = TreeForeignKey('departments.Department',
        blank=True, null=True)

    begin = models.DateField(_('begin'), blank=True, null=True)
    end = models.DateField(_('end'), blank=True, null=True)

    address1 = models.CharField(_('address 1'), max_length=100, blank=True)
    address2 = models.CharField(_('address 2'), max_length=100, blank=True)
    postal_code = models.PositiveIntegerField(_('post code'), blank=True,
        null=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=100, blank=True)

    min_birth_year = models.PositiveIntegerField(blank=True, null=True)
    fee = models.PositiveIntegerField(_('fee'), blank=True, null=True,
        help_text='CHF')
    notes = models.TextField(_('notes'), blank=True)

    participants = models.ManyToManyField('members.Member',
        through='Participant', related_name='camps')

    class Meta:
        verbose_name = _('Camp')
        verbose_name_plural = _('Camps')

    def __unicode__(self):
        return self.title


class ParticipantType(BaseModel):
    title = models.CharField(_('title'), max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Participant type')
        verbose_name_plural = _('Participant types')
        ordering = ('order',)

    def __unicode__(self):
        return self.title


class Participant(BaseModel):
    camp = models.ForeignKey(Camp)
    member = models.ForeignKey('members.Member')
    type = models.ForeignKey(ParticipantType)

    signup_date = models.DateField(_('Signup date'), default=date.today,
        blank=True, null=True)
    confirmation = models.BooleanField(_('confirmation'), default=False)

    payed_fee = models.PositiveIntegerField(blank=True, null=True)
    payed_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')

    def __unicode__(self):
        return self.member.fullname
