from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def simple_is_checked(time_id,title,select_list,room_id):
    # print(title,select_list,room_id)
    for select in select_list:
        if title == select[3] and room_id == select[1]:
            return mark_safe('<td select_id="%s" time_id=%s class="selected">%s</td>'%(select[0],time_id,select[2]))
    else:
        return mark_safe('<td select_id=""  time_id="%s" class="isEmpty"></td>'%time_id)