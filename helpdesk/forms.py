from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from helpdesk.models import Ticket, Report


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'equipment', 'description', 'type', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Слишком длинная тема")
        elif len(title) < 5:
            raise ValidationError("Слишком корткая тема!")

        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 500:
            raise ValidationError("Слишком длинное описание")
        elif len(description) < 25:
            raise ValidationError("Слишком короткое описание!")

        return description


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'status', 'type', 'priority', 'description']


class ReportForm(forms.ModelForm):
    ticket_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Report
        fields = ['speed', 'decision', 'empl_evaluation', 'feedback']

    def init(self, *args, **kwargs):
        ticket_id = kwargs.pop('ticket_id', None)
        super(ReportForm, self).init(*args, **kwargs)

        if ticket_id:
            self.fields['ticket_id'].initial = ticket_id
            ticket = Ticket.objects.get(id=ticket_id)
            self.fields['id_empl'].initial = ticket.empl.id
            self.fields['user_id'].initial = ticket.user.id
