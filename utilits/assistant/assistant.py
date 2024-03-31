import g4f
from g4f.client import Client


def tell_about_workout(user_info):
    engine = g4f.client.Client()

    content = ("Ты как тренер.В ответе кроме программы ничего не пиши. Составь подробную программу тренировок "
               "на месяц для человека с такими параметрами" + str(user_info))
    completion = engine.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}])

    answer = completion.choices[0].message.content
    return answer


def tell_about(gym):
    engine = g4f.client.Client()
    content = ("Расскажи про тренажёр" + str(gym))
    completion = engine.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}])

    answer = completion.choices[0].message.content
    return answer
