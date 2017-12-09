from django import forms
from django.forms import widgets as wd
from app01.models import Question

from app01 import models
class QuestionFrom(forms.ModelForm):
    # question = forms.CharField(error_messages={"required":"不能为空"}
    #             ,widget=widgets.Textarea(attrs={"rows":"3","placeholder":"请输入问题！","class":"form-control Textarea"}))
    #
    # question_types = [
    #     (1, "打分(1～10)"),
    #     (2, "单选"),
    #     (3, "评价"),
    # ]
    # question_type = forms.ChoiceField(widget=widgets.Select(attrs={"class":"form-control"}),choices=question_types)
    #
    # def __init__(self,pid):
    #     obj = Question.objects.filter(id=pid)
    #     if obj:
    #         question_type = forms.ChoiceField(choices=obj.values_list())
    class Meta:
        model = models.Question
        fields = ["caption","tp"]
        error_messages = {
            "caption":{"required":"不能为空"},
        }
        widgets = {
            "caption":wd.Textarea(attrs={"rows":"3","class":"form-control Textarea","placeholder":"请输入问题！"}),
            "tp":wd.Select(attrs={"class":"form-control"}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = models.Option
        fields =["name","score"]
        error_messages = {
            "name":{"required":"不能为空"},
            "score":{"required":"不能为空"},
        }
        widgets = {
            "name":wd.TextInput(attrs={"class":"form-control", "placeholder":"内容"}),
            "score":wd.TextInput(attrs={"class":"form-control", "placeholder":"分值"}),
        }



