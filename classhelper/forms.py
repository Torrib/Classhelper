from django.forms import ModelForm, Textarea
from models import Subject, Assessment, SubjectDocument
from django import forms
from filebrowser.widgets import FileInput

class SubjectForm(ModelForm):

    class Meta:
        model = Subject
        exclude = ['avg_rating', 'no_ratings','ntnu_url' ]
        widgets = {'tags' : forms.SelectMultiple(attrs={'class' : 'chzn-select', 'data-placeholder' : 'Velg tags'}),
                    'examination_type' : forms.Select(attrs={'class' : 'chzn-select'}),
                    'subject_type' : forms.Select(attrs={'class' : 'chzn-select'}),
                    }
    
    def clean_subject_code(self):
        return self.cleaned_data['subject_code'].upper()


class AssessmentForm(ModelForm):
    rating_choices = zip(range(1,11), range(1,11))

    total_rating = forms.ChoiceField(widget=forms.RadioSelect(), choices=rating_choices, help_text="")
    year_taken = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'chzn-select'}), choices=Assessment.get_year_choices())
    
    class Meta:
        model = Assessment
        fields = ['total_rating', 'year_taken',]

class AssessmentOptionalForm(ModelForm):
    rating_choices = zip(range(1,11), range(1,11))
    
    lecture_quality = forms.ChoiceField(widget=forms.RadioSelect(), choices=rating_choices, help_text="", required=False)
    difficulty = forms.IntegerField(widget=forms.TextInput(attrs={'type' : 'range', "min" : "0", "max" : "10", "class" : "slider", "value" : "0" }))
    time_demanding = forms.IntegerField(widget=forms.TextInput(attrs={'type' : 'range', "min" : "0", "max" : "10", "class" : "slider", "value" : "0"}))
    theory_vs_practice = forms.IntegerField(widget=forms.TextInput(attrs={'type' : 'range', "min" : "0", "max" : "10", "class" : "slider", "value": "0"}))

    class Meta:
        model = Assessment
        fields = ['difficulty', 'lecture_quality', 'time_demanding', 'theory_vs_practice', 'comment',]

class SubjectDocumentForm(ModelForm):
    
    document_type = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'chzn-select'}))
    

    class Meta:
        model = SubjectDocument
        exclude = ['subject',]
        widget = { 'document' : FileInput, }
