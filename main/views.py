import datetime

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse


class DATE(dict):
    def __init__(self, **kwargs):
        """список дат с названиями"""
        super().__init__()
        for k, v in kwargs.items():
            start, stop = v
            self[k] = datetime.date(*start), datetime.date(*stop)

    def compare(self, date_):
        """по введённой дате определяет её принадлежность к диапазону дат"""
        d_ = datetime.date(*date_)
        for sign in self:
            start, stop = self[sign]
            if start <= d_ <= stop:  # определяет
                return sign  # выводит к какому диапазону она принадлежит


# Есть список церковных постов с датами и названиями
signs_date = DATE(
    aries=[(2021, 3, 21), (2021, 4, 20)],
    taurus=[(2021, 4, 21), (2021, 5, 21)],
    gemini=[(2021, 5, 22), (2021, 6, 21)],
    cancer=[(2021, 6, 22), (2021, 7, 22)],
    leo=[(2021, 7, 23), (2021, 8, 21)],
    virgo=[(2021, 8, 22), (2021, 9, 23)],
    libra=[(2021, 9, 24), (2021, 10, 23)],
    scorpio=[(2021, 10, 24), (2021, 11, 22)],
    sagittarius=[(2021, 11, 23), (2021, 12, 22)],
    capricorn=[(2021, 12, 23), (2022, 1, 20)],
    aquarius=[(2021, 1, 21), (2021, 2, 19)],
    pisces=[(2021, 2, 20), (2021, 3, 20)],

)

zodiac_description = {"aries": "Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля)",
                      "taurus": "Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая)",
                      "gemini": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня)",
                      "cancer": "Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля)",
                      "leo": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа)",
                      "virgo": "Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября)",
                      "libra": "Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября)",
                      "scorpio": "Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября)",
                      "sagittarius": "Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря)",
                      "capricorn": "Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января",
                      "aquarius": "Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля)",
                      "pisces": "Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта)"
                      }
horoscope_signs = {
    'fire': ['aries', 'leo', 'sagittarius'],
    'earth': ['taurus', 'virgo', 'capricorn'],
    'air': ['gemini', 'libra', 'aquarius'],
    'water': ['cancer', 'scorpio', 'pisces']
}


def index(request):
    zodiac_by_num = list(zodiac_description)
    # rez += f"<li> <a href='{url_nam}'>{sign.title()} </a> </li>"
    data = {
        'zodiac_list': zodiac_by_num
    }
    return render(request, 'main/index.html', context= data)


def get_info(request, zodiac_name: str):
    description = zodiac_description.get(zodiac_name, None)
    data = {
        'description_zodiac': description,
        'sign': zodiac_name
    }
    response = render_to_string('main/info_zodiac.html')
    return render(request, 'main/info_zodiac.html', data)


def get_info_by_num(request, zodiac_num: int):
    zodiac_by_num = list(zodiac_description)
    if zodiac_num > len(zodiac_description):
        return HttpResponseNotFound('It is not zodiak')
    zodiac_name = zodiac_by_num[zodiac_num - 1]
    url_nam = reverse("horoskop", args=(zodiac_name,))
    return HttpResponseRedirect(url_nam)


def get_types(request):
    zodiac_by_num = list(horoscope_signs)
    li_name = ''
    for sign in zodiac_by_num:
        url_nam = reverse("type", args=[sign])
        li_name += f"<li> <a href='{url_nam}'>{sign.title()} </a> </li>"
    response = f"""
        <ol>
            {li_name}
        </ol>
        """
    return HttpResponse(response)


def get_elem(request, element):
    li_elem = []
    for key, value in horoscope_signs.items():
        if key == element:
            li_elem = value
    li_name = ''
    for sign in li_elem:
        url_nam = reverse("horoskop", args=[sign])
        li_name += f"<li> <a href='{url_nam}'>{sign.title()} </a> </li>"
    response = f"""
        <ol>
            {li_name}
        </ol>
        """
    return HttpResponse(response)


def get_sign(request, month, day):
    try:
        rez = signs_date.compare((2021, month, day))
        url_nam = reverse("horoskop", args=[rez])
        return HttpResponseRedirect(url_nam)
    except ValueError:
        return HttpResponseNotFound(f'unknown date<br>month: {month}<br>day: {day}')
