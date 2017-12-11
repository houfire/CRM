from django.shortcuts import render,HttpResponse
from reservation.models import *
import json
import datetime

def roomreservation(request):
    '''
    会议室预定
    '''

    if request.method == "GET":


        room_list=Room.objects.all()
        time_list = Time.objects.all()

        find_data=request.GET.get("find_data")
        if find_data:
            year,month,day = find_data.split("-")
        else:
            nowday=datetime.datetime.now()
            year=nowday.year
            month=nowday.month
            day=nowday.day
        datatime_obj=Date.objects.filter(datetime__year=year,
                            datetime__month=month,
                            datetime__day=day)
        print("datatime_obj",datatime_obj)
        select_list = Select.objects.filter(data=datatime_obj).values_list("id","room_id","user__name","time__title")
        for x in select_list:
           print(x)
        context={"room_list":room_list,"time_list":time_list,"select_list":select_list,"datatime_obj":datatime_obj}
        return render(request,'roomreservation.html',context)
    else:
        upDate=json.loads(request.body)
        # user_id=request.session.get("user_id")  获取用户id
        user_id = 2
        print(request.body)
        print(upDate)
        choice_list = upDate.get("add_list")
        nowData = upDate.get("nowData")
        year,month,day=nowData.split("-")

        datatime_obj = Date.objects.filter(datetime__year=year, datetime__month=month,datetime__day=day)
        if datatime_obj:
            dataObj = datatime_obj.first().id
        else:
            dataObj=Date.objects.create(datetime=datetime.datetime.strptime(nowData,"%Y-%m-%d"))
        for choice in choice_list:
            Select.objects.create(user_id=user_id,data_id=dataObj,**choice)
        return HttpResponse("OK")
