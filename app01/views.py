from django.db.models import Count
from django.shortcuts import render
from .models import *
from .forms import *
from django.forms import ModelForm
def index(request):

    questionnaire_list=Questionnaire.objects.all()
    context={"questionnaire_list":questionnaire_list}
    return render(request, 'index.html',context)


# class QuestionFrom(ModelForm):
#     class Meta:
#         model = Question
#         fields = ['caption','tp']

def questionnaire(request,naire_id):

    # question_list=Question.objects.filter(questionnaire_id=naire_id)
    # form_list=[]
    # if  not question_list:
    #     form = QuestionFrom()
    #     form_list.append(form)
    # else:
    #      for question in question_list:
    #         form =QuestionFrom(instance=question)
    #         form_list.append(form)
    # return render(request, 'questionnaireAdd.html', {"questionFrom": form_list})
    def inner():
        question_list = Question.objects.filter(questionnaire_id=naire_id)
        if  not question_list:
            # 新创建的问卷，其中还么有创建问题
            form = QuestionFrom()
            yield {'form': form, 'question': None, 'option_class': 'hide', 'options': None}
        else:
            # 含问题的问卷
            for question in question_list:
                form = QuestionFrom(instance=question)
                temp = {'form': form, 'question': question, 'option_class': 'hidden', 'options': None}
                if question.tp == 2:
                    temp['option_class'] = ''
                    # 获取当前问题的所有选项？
                    def inner_loop(quee):
                        option_list = Option.objects.filter(qs=quee)
                        for option in option_list:
                            yield {'form': OptionForm(instance=option), 'option': option}
                    temp['options'] = inner_loop(question)
                yield temp
    return render(request, 'questionnaireAdd.html', {"questionFrom": inner()})