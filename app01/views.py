from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, HttpResponse

from django.forms import Form
from django.forms import widgets
from django.forms import fields

from .models import *
from .forms import *
import json
from django.forms import ModelForm


def index(request):
    questionnaire_list = Questionnaire.objects.all()
    context = {"questionnaire_list": questionnaire_list}
    return render(request, 'index.html', context)


# class QuestionFrom(ModelForm):
#     class Meta:
#         model = Question
#         fields = ['caption','tp']
def questionnaire(request, naire_id):
    '''
    添加修改问题
    '''

    def inner():
        question_list = Question.objects.filter(questionnaire_id=naire_id)
        if not question_list.exists():
            # 新创建的问卷，其中还么有创建问题
            form = QuestionFrom()
            yield {'form': form, 'question': None, 'options': None}
        else:
            # 含问题的问卷
            for question in question_list:
                form = QuestionFrom(instance=question)
                temp = {'form': form, 'question': question, 'options': None}
                if question.tp == 2:
                    # 获取当前问题的所有选项？
                    def inner_loop(quee):
                        option_list = Option.objects.filter(qs=quee)
                        for option in option_list:
                            yield {'form': OptionForm(instance=option), 'option': option}

                    temp['options'] = inner_loop(question)
                yield temp

    if request.method == "GET":
        request.session["naire_id"] = naire_id

        return render(request, 'questionnaire.html', {"questionFrom": inner()})
    else:
        question_dict = json.loads(request.body)
        try:
            with transaction.atomic():
                question_id_list = []  # 当前问卷的所有问题的id，为了去除的在前端已删除的问题
                option_id_list = []  # 当前问卷所有选项的id
                for quest in question_dict["question_list"]:
                    print(quest)
                    print("question_id---", quest["question_id"], type(quest["question_id"]))
                    print("question_content---", quest["question_content"])
                    print("question_content.tp---", quest["question_content"]["tp"],
                          type(quest["question_content"]["tp"]))
                    question_id = quest.get("question_id")
                    question_content = quest.get("question_content")
                    options = quest.get("options")
                    questForm = QuestionFrom(quest.get("question_content"))
                    if questForm.is_valid():
                        print("success")
                        if question_id:
                            print("question update-------")
                            Question.objects.filter(id=question_id).update(**question_content)
                            question_id_list.append(question_id)
                            # #如果question_content.tp 不是单选，则删除对应option选项
                            # if question_content.get("tp") != 2:
                            #     Option.objects.filter(qs_id=question_id).delete()
                        else:
                            print("question create-------")
                            question_obj = Question.objects.create(**question_content, questionnaire_id=naire_id)
                            question_id_list.append(question_obj.id)
                    else:
                        raise print("question  输入有误！")
                    if options:
                        print("options has value------")
                        for opt in options:
                            option_id = opt.get("option_id")
                            option_content = opt.get("option_content")

                            optForm = OptionForm(option_content)
                            if optForm.is_valid():
                                if option_id:
                                    print("option update-------")
                                    Option.objects.filter(id=option_id).update(**option_content)
                                    option_id_list.append(option_id)
                                else:
                                    print("option create-------")
                                    # 判断是否新创建的问题
                                    if question_id:
                                        option_obj = Option.objects.create(**option_content, qs_id=question_id)
                                    else:
                                        option_obj = Option.objects.create(**option_content, qs=question_obj)
                                    option_id_list.append(option_obj.id)
                            else:
                                raise print("option  输入有误！")
                else:
                    Question.objects.filter(questionnaire_id=naire_id).exclude(id__in=question_id_list).delete()
                    Option.objects.filter(qs_id__in=question_id_list).exclude(id__in=option_id_list).delete()
                    return HttpResponse("OK")
        except Exception:
            return HttpResponse("Fail")


def questionnaireAdd(request):
    pass


def investigation(request, naire_id):
    '''
    开始问卷调查
    '''
    field_dict = {}
    request.session["naire_id"] = naire_id
    print(naire_id)
    question_list = Question.objects.filter(questionnaire_id=naire_id)
    for question in question_list:
        if question.tp == 1:
            field_dict["val_%s" % question.id] = fields.ChoiceField(label=question.caption,
                                                                    error_messages={"required": "请选择！"},
                                                                    choices=[(x, x) for x in range(1, 11)],
                                                                    widget=widgets.RadioSelect)
        elif question.tp == 2:
            field_dict["option_id_%s" % question.id] = fields.ChoiceField(label=question.caption,
                                                                          error_messages={"required": "请选择！"},
                                                                          choices=question.option_set.all().values_list(
                                                                              "id", "name"), widget=widgets.RadioSelect)
        elif question.tp == 3:
            field_dict["content_%s" % question.id] = fields.CharField(label=question.caption, min_length=15,
                                                                      error_messages={"required": "不能为空！",
                                                                                      "min_length": "不能少于15个字"},
                                                                      widget=widgets.Textarea(
                                                                          attrs={"cols": "40", "rows": "3",
                                                                                 "class": "form-control Textarea",
                                                                                 "placeholder": "请输入建议！，最少15个字"}))

    # type创建类对象
    TestForm = type('TestForm', (Form,), field_dict)

    if request.method == 'GET':
        print(field_dict)
        form = TestForm()
        return render(request, 'investigation.html', {"form": form})

    else:

        # answer_list = json.loads(request.body)
        # print(answer_list)
        # form = TestForm(answer_list)
        data = request.POST
        print(data)
        form = TestForm(data)
        if form.is_valid():
            print("success")

            for key,val in data.items():
                aa = {}
                if key =="csrfmiddlewaretoken":
                    continue
                ans_k,que_id=key.rsplit("_",1)
                aa[ans_k] = val
                print("aa",aa)
                Answer.objects.create(stu_id=1, question_id=que_id, questionnaire_id=naire_id, **aa)
            return HttpResponse("ok")
        return render(request, 'investigation.html', {"form": form})




def aaa(request, naire_id):
    queryset = Question.objects.all().iterator()
    for x in queryset:
        print(x.caption, x.tp)
    for x in queryset:
        print(x.tp)
    # query_list=[x for x in queryset]
    # print(query_list[1])
    # print(query_list[2])
    # print(query_list[0])
    # print("queryset[2]",queryset[2])
    # print("queryset[0]",queryset[0])



    # question_list = Question.objects.filter(questionnaire_id=naire_id)
    # print("是否有数据",question_list.exists())
    return HttpResponse("OK")
