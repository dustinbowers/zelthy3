from datetime import datetime

from django import forms
from django.shortcuts import redirect

from ....packages.crud.forms import BaseSimpleForm
from ....packages.crud.form_fields import ModelField, CustomSchemaField

from .models import ResponsesModel

class ResponseFormBase(BaseSimpleForm):

    def __init__(self, *args, **kwargs):

        super(ResponseFormBase, self).__init__(*args, **kwargs)

        crud_fields, crud_declared_fields, title = self.crud_view_instance.get_questions()

        self.fields.update(crud_fields)
        self.declared_fields.update(crud_declared_fields)

        print(self.declared_fields['Caller Identity-s_select'].__dict__)

        self.Meta.title = title


    def save(self, commit=True):
        # instance = super(ResponseFormBase, self).save(commit=False)
        response = self.crud_view_instance.take_response(self.cleaned_data)
        if self.crud_view_instance.success_url:
            return redirect(self.crud_view_instance.success_url)
        else:
            return response


    class Meta:
        model = ResponsesModel