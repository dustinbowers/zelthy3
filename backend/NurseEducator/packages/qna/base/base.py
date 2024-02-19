from copy import deepcopy

from ....packages.crud.base import BaseFormOnlyView

from .forms import ResponseFormBase
from .models import QuestionnaireModel, QuestionsModel, ResponsesModel, ResponseAnswerModel

from ....packages.crud.form_fields import ModelField

from zelthy.core.api import get_api_response
from zelthy.apps.object_store.models import ObjectStore

from urllib.parse import urlparse, parse_qs

from datetime import datetime, timedelta

from django import forms
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView


class QnAAPIView(APIView):

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        success = True
        status_code = 200
        if action == "get_questionnaire_details":
            questionnaire  = None
            can_fill = True
            try:
                if request.GET.get("questionnaire_key", ""):
                    questionnaire = QuestionnaireModel.objects.get(key=request.GET.get("questionnaire_key", ""))
                elif request.GET.get("questionnaire_uuid", ""):
                    questionnaire = QuestionnaireModel.objects.get(object_uuid=request.GET.get("questionnaire_uuid", ""))
                
                app_object_uuid = request.GET.get("app_object_uuid", "")
                if questionnaire:
                    config = questionnaire.config
                    if config:
                        if not config.get('is_multiple_allowed_user', False):
                            responses = ResponsesModel.objects.filter(questionnaire=questionnaire, created_by=self.request.user)
                            if responses.exists():
                                can_fill = False

                        if app_object_uuid and not config.get('is_multiple_allowed_object', False):
                            responses = ResponsesModel.objects.filter(questionnaire=questionnaire, app_object=app_object_uuid)
                            if responses.exists():
                                can_fill = False

                    result = {
                        'data': {
                            'questionnaire_uuid': str(questionnaire.object_uuid),
                            'config': questionnaire.config,
                            'key': questionnaire.key,
                            'title': questionnaire.title,
                            'decription': questionnaire.description,
                            'can_fill': can_fill
                        },
                        'message': 'success'
                    }
                    
                else:
                    result = {
                        'message': 'Unknown Identifier key'
                    }
                    success = False
                    status_code = 400    

            except QuestionnaireModel.DoesNotExist:
                result = {
                    'message': 'Invalid Identifier value'
                }
                success = False
                status_code = 400
            except Exception as e:
                import traceback
                print(traceback.print_exc())
                print(str(e))
                result = {
                    'message': 'Something Bad Happend'
                }
                success = False
                status_code = 500


        elif action == "get_response_details":

            try:

                query = Q()
                
                if request.GET.get("response_uuid", ""):
                    query = query | Q(object_uuid=request.GET.get("response_uuid", ""))
                if request.GET.get("questionnaire_uuid", ""):
                    query = query | Q(questionnaire__object_uuid=request.GET.get("questionnaire_uuid", ""))
                if request.GET.get("questionnaire_key", ""):
                    query = query | Q(questionnaire__key=request.GET.get("questionnaire_key", ""))
                if request.GET.get("app_object_uuid", ""):
                    query = (query) & Q(app_object=request.GET.get("app_object_uuid", ""))
                
                if query == Q():
                    result = {
                        'message': 'Invalid Identifier value'
                    }
                    success = False
                    status_code = 400

                responses = ResponsesModel.objects.filter(query)

                data = []
                result = {
                    'message': 'success', 
                }

                for response in responses:
                    data.append({
                        'app_object_uuid': str(response.app_object),
                        'questionnaire_uuid': str(response.questionnaire.object_uuid),
                        'response_uuid': str(response.object_uuid)
                    })
                result['data'] = data
            
            except Exception as e:
                print(str(e))
                result = {
                    'message': 'Something Bad Happend'
                }
                success = False
                status_code = 500

               
        
        else:
            result = {
                'message': 'Invalid action'
            }
            success = False
            status_code = 400


        return get_api_response(True, result, 200)

            


class TakeResponseBaseView(BaseFormOnlyView):
    
    form = ResponseFormBase
    page_title = "QnA"
    success_url = ""



    def get_success_url(self):
        back_url = self.request.META.get('HTTP_REFERER')
        parsed_url = urlparse(back_url)
        query_params = parse_qs(parsed_url.query)
        if query_params.get('redirect_url'):
            return query_params.get('redirect_url')[0].replace('%3F', '?').replace('%26', '&')

        

    success_url = property(get_success_url)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(TakeResponseBaseView, self).get_context_data(*args, **kwargs)
    #     context["display_sidebar"] = False
    #     return context



    def get_questions(self):
        mapper = {
            's_text': {
                'fields': forms.CharField(),
                'declared_fileds': ModelField()
            },
            'b_text': {
                'fields': forms.CharField(),
                'declared_fileds': ModelField()
            },
            'date': {
                'fields': forms.DateField(),
                'declared_fileds': ModelField()
            },
            'datetime': {
                'fields': forms.DateTimeField(),
                'declared_fileds': ModelField()
            },
            's_select': {
                'fields': forms.ChoiceField(),
                'declared_fileds': ModelField()
            },
            'm_select': {
                'fields': forms.MultipleChoiceField(),
                'declared_fileds': ModelField()
            },
            'bool': {
                'fields': forms.BooleanField(),
                'declared_fileds': ModelField()
            }
        }

        answer_mapper = {
            's_text': 'answer_text',
            'b_text': 'answer_long_text',
            'bool': 'answer_boolean',
            's_select': 'answer_select_option',
            'm_select': 'answer_select_option',
            'date': 'answer_date',
            'datetime': 'answer_datetime'
        }

        fields = {}
        declared_fields = {}
        questionnaire_uuid = self.kwargs.get('questionnaire_uuid', '')
        response_obj = None
        if self.kwargs.get('response_uuid'):
            response_obj = ResponsesModel.objects.get(object_uuid=self.kwargs.get('response_uuid'))
            questionnaire_uuid = str(response_obj.questionnaire.object_uuid)
        if questionnaire_uuid:
            try:
                questionnaire = QuestionnaireModel.objects.get(object_uuid=questionnaire_uuid)
                config = questionnaire.config
                if not config.get('is_multiple_allowed_user', True):
                    if ResponsesModel.objects.filter(created_by=self.request.user, questionnaire=questionnaire).exists():
                        raise Http404
                if not config.get('is_multiple_allowed_object', True):
                    if self.kwargs.get('app_object_uuid'):
                        if ResponsesModel.objects.filter(app_object=self.kwargs.get('app_object_uuid'), questionnaire=questionnaire).exists():
                            raise Http404
                questions = QuestionsModel.objects.filter(questionnaire=questionnaire)
                for question in questions:
                    field_map = mapper.get(question.response_type, {})
                    fields_value = deepcopy(field_map.get('fields'))
                    declared_fields_value = deepcopy(field_map.get('declared_fileds'))

                    # print(question.question)
                    declared_fields_value.properties['label'] = question.question
                    declared_fields_value.properties['placeholder'] = "Enter "+question.question

                    fields_value.required=question.is_required
                    declared_fields_value.properties['required'] = question.is_required

                    if question.is_required:    
                        declared_fields_value.properties['required_msg'] = question.question+" is required"
                        # fields_value.error_messages={
                        #     'required': question.question+" is required"
                        # }

                    if question.response_type in ["s_select", "m_select"]:
                        options = []
                        if question.options:
                            for option in question.options:
                                options.append((option, option))
                            answer_mapper.update({
                                's_select': 'answer_select_option',
                                'm_select': 'answer_select_option'
                            })
                        elif question.options_uuid:
                            for option_uuid in question.options_uuid:
                                obj = ObjectStore.get_object(option_uuid)
                                options.append((option_uuid, obj.__str__()))
                            answer_mapper.update({
                                's_select': 'answer_select_object',
                                'm_select': 'answer_select_object'
                            })
                        fields_value.choices = options

                    if response_obj:
                        try:
                            actual_response = ResponseAnswerModel.objects.get(question=question, response=response_obj)
                            data_field = answer_mapper.get(question.response_type, None)
                            value = getattr(actual_response, data_field)
                            value = [value] if question.response_type in ["s_select", "m_select"] and not type(value) == list else value
                            fields_value.initial = value
                            declared_fields_value.extra_schema = {
                                "readOnly": True
                            }
                            declared_fields_value.properties['readonly'] = True
                            # fields_value.widget.attrs['readonly'] = 'readonly'
                        except Exception as e:
                            print(str(e))


                    fields.update({
                        str(question.question)+"-"+question.response_type: fields_value
                    })
                    declared_fields.update({
                        str(question.question)+"-"+question.response_type: declared_fields_value
                    })
                
                print(fields)
                print(declared_fields)
            except QuestionnaireModel.DoesNotExist:
                raise Http404
        else:
            raise Http404

        return fields, declared_fields, questionnaire.title


    def take_response(self, form_data):
        mapper = {
            's_text': 'answer_text',
            'b_text': 'answer_long_text',
            'bool': 'answer_boolean',
            's_select': 'answer_select_option',
            'm_select': 'answer_select_option',
            'date': 'answer_date',
            'datetime': 'answer_datetime'
        }
        questionnaire_uuid = self.kwargs.get('questionnaire_uuid', '')
        if questionnaire_uuid:
            try:
                questionnaire = QuestionnaireModel.objects.get(object_uuid=questionnaire_uuid)
            except QuestionnaireModel.DoesNotExist:
                raise Http404
        else:
            raise Http404
        response = ResponsesModel.objects.create(questionnaire=questionnaire)
        if self.kwargs.get('app_object_uuid'):
            obj = ObjectStore.get_object(self.kwargs.get('app_object_uuid'))
            if obj:
                response.app_object = str(self.kwargs.get('app_object_uuid'))
                response.save()
            else:
                raise Http404
        questions = QuestionsModel.objects.filter(questionnaire=questionnaire)
        for question in questions:
            question_key = str(question.question)+"-"+question.response_type
            data = form_data.get(question_key)
            answer_type = question.response_type
            if answer_type in ['s_select', 'm_select']:
                if question.options:
                    mapper.update({
                        's_select': 'answer_select_option',
                        'm_select': 'answer_select_option'
                    })
                elif question.options_uuid:
                    mapper.update({
                        's_select': 'answer_select_object',
                        'm_select': 'answer_select_object'
                    })

            answer = {
                'answer_type': answer_type,
                'response': response,
                'question': question
            }

            if answer_type in ['s_select', 'm_select']:
                if not type(data) == list:
                    data = [data]
                
            answer[mapper[answer_type]] = data

            response_answer = ResponseAnswerModel.objects.create(**answer)


        return True


    
    