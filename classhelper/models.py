# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import date

from filebrowser.fields import FileBrowseField

class Tag(models.Model):
    name = models.CharField(_(u'Navn'), max_length=30)
    
    def __unicode__(self):
        return self.name

class Subject(models.Model):
    examination_type_choices = (
        ('N', 'Normal'),
        ('M', 'Multiple choice'),
        ('TF', 'True / False'),
        ('H', _('Hjelpemidler')),
        ('HI', _('Hjemme eksamen')),
        ('A', _('Annet')),
    )

    subject_type_choices = (
        ('O', _(u'Obligatorisk')),
        ('V', _(u'Valgfag')),
        ('P', _(u'Perspektivemne')),
    )

    subject_code = models.CharField(_("Emnekode"), max_length=10)
    subject_name = models.CharField(_("Emnenavn"), max_length=200)
    subject_type = models.CharField(_("Type"), choices = subject_type_choices, default = 'O',  max_length=50)
    ntnu_url = models.URLField(_("URL"))
    examination_type = models.CharField(_("Eksamens type"), max_length = 2, choices = examination_type_choices, default = 'N')
    tags = models.ManyToManyField(Tag, related_name=_(u'Tags'), help_text="", null=True, blank=True)    

    #additional info
    assignments = models.TextField(_(u"Øvingsopplegg"), null = True, blank = True)
    comment = models.TextField(_("Komentar"), null=True, blank = True)

    def get_rating(self): 
        ratings = self.rating_set.all()
        if ratings:
            return self.rating_set.get()
        else:
            return Rating(subject = self)

    def update_ratings(self, updates):
        rating = self.get_rating()
        rating.update(updates)
        rating.save()


    @models.permalink
    def get_absolute_url(self):
        return( 'subject_details', (), {'subject_id' : self.id})

    def __unicode__(self):
        return self.subject_code
    
    def save(self, *args, **kwargs):
        self.ntnu_url = u"http://www.ntnu.no/studier/emner/%s" % (self.subject_code)
        super(Subject, self).save()

#TODO karakterdata, filer, øvinger, eksamenssett


class Assessment(models.Model):
    rating_choices = zip(range(1,11), range(1,11))
    slider_choices = zip(range(0,11), range(0,11))

    total_rating = models.SmallIntegerField(_('Total vurdering'), choices = rating_choices)
    year_taken = models.SmallIntegerField(_(u'År tatt'))


    #Optional
    difficulty = models.SmallIntegerField(_('Vanskelighets grad'), choices = slider_choices, blank = True, null = True)
    time_demanding = models.SmallIntegerField(_('Tids krevende'), choices = slider_choices, blank = True, null = True)
    lecture_quality = models.SmallIntegerField(_('Forelesnings kvalitet'), choices = rating_choices, blank = True, null = True)
    theory_vs_practice = models.SmallIntegerField(_('Teoretisk / praktisk'), choices = slider_choices, blank = True, null = True)

    user = models.ForeignKey(User, null=True, blank=True)

    comment = models.TextField(_("Komentar"), null=True, blank=True)
    subject = models.ForeignKey(Subject)

    @staticmethod
    def get_year_choices():
        year = date.today().year
        return zip(range(year-3, year +1), range(year-3, year +1))

class Rating(models.Model):
    subject = models.ForeignKey(Subject)

    total_rating = models.SmallIntegerField(blank = True, null = True, default = 0)
    total_rating_total = models.SmallIntegerField(blank = True, null = True, default = 0)
    total_rating_count = models.SmallIntegerField(blank = True, null = True, default = 0)

    difficulty = models.SmallIntegerField(blank = True, null = True, default = 0)
    difficulty_total = models.SmallIntegerField(blank = True, null = True, default = 0)
    difficulty_count = models.SmallIntegerField(blank = True, null = True, default = 0)
    
    time_demanding = models.SmallIntegerField(blank = True, null = True, default = 0)
    time_demanding_total = models.SmallIntegerField(blank = True, null = True, default = 0)
    time_demanding_count = models.SmallIntegerField(blank = True, null = True, default = 0)
    
    lecture_quality = models.SmallIntegerField(blank = True, null = True, default = 0)
    lecture_quality_total = models.SmallIntegerField(blank = True, null = True, default = 0)
    lecture_quality_count = models.SmallIntegerField(blank = True, null = True, default = 0)

    theory_vs_practice = models.SmallIntegerField(blank = True, null = True, default = 0)
    theory_vs_practice_total = models.SmallIntegerField(blank = True, null = True, default = 0)
    theory_vs_practice_count = models.SmallIntegerField(blank = True, null = True, default = 0)

    def update(self, updates): 
        if updates.get('total_rating', None):
            self.total_rating_total += int(updates.get('total_rating'))
            self.total_rating_count += 1
            self.total_rating = self.total_rating_total / self.total_rating_count
        if updates.get('difficulty', None):
            self.difficulty_total += int(updates.get('difficulty'))
            self.difficulty_count += 1
            self.difficulty = self.difficulty_total / self.difficulty_count
        if updates.get('time_demanding', None):
            self.time_demanding_total += int(updates.get('time_demanding'))
            self.time_demanding_count += 1
            self.time_demanding = self.time_demanding_total / self.time_demanding_count
        if updates.get('lecture_quality', None):
            self.lecture_quality_total += int(updates.get('lecture_quality'))
            self.lecture_quality_count += 1
            self.lecture_quality = self.lecture_quality_total / self.lecture_quality_count
        if updates.get('theory_vs_practice', None):
            self.theory_vs_practice_total += int(updates.get('theory_vs_practice'))
            self.theory_vs_practice_count += 1
            self.theory_vs_practice = self.theory_vs_practice_total / self.theory_vs_practice_count

class Grades(models.Model):
    subject = models.ForeignKey(Subject)

    semester_code = models.CharField(max_length=8)

    a = models.SmallIntegerField(default = 0)
    b = models.SmallIntegerField(default = 0)
    c = models.SmallIntegerField(default = 0)
    d = models.SmallIntegerField(default = 0)
    e = models.SmallIntegerField(default = 0)
    f = models.SmallIntegerField(default = 0)



class SubjectDocument(models.Model):
    document_type_choices = (
        ('E', _(u'Eksamen')),
        ('O', _(u'Øving')),
        ('K', _(u'Kompendie')),
        ('N', _(u'Forelesnings materiale')),
        ('A', _(u'Annet')),
    )

    subject = models.ForeignKey(Subject)
    document_type = models.CharField(_(u'Type'), max_length=200, choices=document_type_choices, default='E')
    document = FileBrowseField('PDF', max_length=500, directory='classhelper/', extensions=['.pdf', '.doc',])

    def __unicode__(self):
        return "%s - %s" % (self.subject.subject_code, self.id)
