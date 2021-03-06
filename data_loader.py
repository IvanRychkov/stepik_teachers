from data import data

import models as m


def load_data(db):
    try:
        # Загружаем дни недели в базу
        for wd, name in data.weekdays.items():
            db.session.add(m.Weekday(short_name=wd, ru_name=name))

        # Загружаем цели
        for g in data.goals:
            db.session.add(m.Goal(**g))

        # Загружаем преподавателей
        if m.Teacher.query.count() == 0:
            goals = m.Goal.query.all()
            for teacher in data.teachers:
                t = m.Teacher(
                    id=teacher['id'],
                    name=teacher['name'],
                    about=teacher['about'],
                    rating=teacher['rating'],
                    picture=teacher['picture'],
                    price=teacher['price'],
                    free=teacher['free']
                )
                # Дополняем связи с целями
                for g in goals:
                    if g.name in teacher['goals']:
                        t.goals.append(g)

                db.session.add(t)
        db.session.commit()
        print('initial data loaded')
    except:
        db.session.rollback()
        print('data already exists')
