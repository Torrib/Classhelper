from django.contrib import messages
from models import Subject, Assessment, Tag
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from forms import SubjectForm, AssessmentForm, AssessmentOptionalForm, SubjectDocumentForm
from django.core import serializers

def index(request):
    subjects = Subject.objects.all()
        
    tags = Tag.objects.all()
    return render(request, 'subject_list.html', {'subjects' : subjects, 'tags' : tags})

def subjectview(request, subject_id=None):
    if subject_id == None:
        subject = Subject()
    else:
        subject = get_object_or_404(Subject, pk=subject_id)
        old_subject_code = subject.subject_code

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            subject_code = cleaned_data['subject_code']
            if subject_id:
                if subject_code == old_subject_code:
                    form = form.save()
                    messages.success(request, 'Subject edited')
                    return redirect(index)
                else:
                    messages.error(request, 'The subject code cannot edited')
            else:
                subjects = Subject.objects.filter(subject_code=subject_code)
                if subjects.count() > 0:
                    messages.error(request, 'Subject already exists')
                else:
                    form = form.save()
                    messages.success(request, 'Subject added')
                    return redirect(index)
        else:
           form = SubjectForm(request.POST, auto_id=True)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'subjectview.html', {'form' : form})

    
def subject_details(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    return render(request, 'subject_details.html', {'subject' : subject, 'labels' : get_labels_for(subject)})


def assessmentview(request, subject_id=None):
    assessment_id = None
    if assessment_id == None:
        assessment = Assessment()
    else:
        assessment = get_object_or_404(Assessment, pk=assessment_id)

    if subject_id != None:
        subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment)
        optional_form = AssessmentOptionalForm(request.POST)
        if form.is_valid() and optional_form.is_valid():
            #TODO knytte bruker
            cleaned_main = form.cleaned_data
            cleaned_optional = optional_form.cleaned_data
            add_assessment(cleaned_main, cleaned_optional, subject)
            return redirect(subject_details, subject_id)
        else:
            messages.error(request, 'Invalid inputs')
            form = AssessmentForm(request.POST, auto_id=True)

    else:
        form = AssessmentForm(instance=assessment)
        optional_form = AssessmentOptionalForm()
    return render(request, 'assessmentview.html', {'form' : form, 'optional_form' : optional_form})

def document_view(request, subject_id=None):

    if request.method == 'POST':
        form = SubjectDocumentForm(request.POST)
        if form.is_valid():
            subject = get_object_or_404(Subject, pk=subject_id)
            form.subject = subject
            form.save()
            return redirect(subject_details, subject_id)
        else:
            messages.error(request, 'Invalid inputs')
            form = SubjectDocumentForm(request.POST, auto_id=True)
    else:
        form = SubjectDocumentForm()

    return render(request, 'documentview.html', {'form' : form })

def get_labels_for(model, cap=True, esc=True):
    from django.template.defaultfilters import capfirst
    from django.utils.html import escape
    labels = {}
    for field in model._meta.fields:
        label = field.verbose_name
        if cap:
            label = capfirst(label)
        if esc:
            label = escape(label)
        labels[field.name] = label
    return labels

def add_assessment(cleaned_main, cleaned_optional, subject): #user
    updates = {}
    assessment = Assessment()
    
    assessment.subject = subject
    assessment.total_rating = cleaned_main['total_rating']
    assessment.year_taken = cleaned_main['year_taken']
                
    updates['total_rating'] =  assessment.total_rating

    if cleaned_optional['difficulty']:
        if cleaned_optional['difficulty'] > 0:
            assessment.difficulty = cleaned_optional['difficulty']
            updates['difficulty'] = assessment.difficulty
    if cleaned_optional['time_demanding']:
        if cleaned_optional['time_demanding'] > 0:
            assessment.time_demanding = cleaned_optional['time_demanding']
            updates['time_demanding'] = assessment.time_demanding
    if cleaned_optional['lecture_quality']:
        assessment.lecture_quality = cleaned_optional['lecture_quality']
        updates['lecture_quality'] = assessment.lecture_quality
    if cleaned_optional['theory_vs_practice']:
        if cleaned_optional['theory_vs_practice'] > 0:
            assessment.theory_vs_practice = cleaned_optional['theory_vs_practice']
            updates['theory_vs_practice'] =  assessment.theory_vs_practice
    if cleaned_optional['comment']:
        assessment.comment = cleaned_optional['comment']
    assessment.subject.update_ratings(updates)
    subject.save()
    assessment.save()

def get_JSON_grades(request):
    json = None
    if request.method == u'GET':
        get = request.GET
        if get.has_key(u'subject_id'):
            subject_id = int(get[u'subject_id'])
            subject = get_object_or_404(Subject, pk=subject_id)
            grades = subject.grades_set.all().order_by('semester_code')
            json = serializers.serialize('json', grades)
    return HttpResponse(json, mimetype='application/json')

def get_JSON_subjects(request):
    subjects = Subject.objects.all()
    json = serializers.serialize('json', subjects)
    return HttpResponse(json, mimetype='application/json')
