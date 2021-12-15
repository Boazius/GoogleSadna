import json
from sqlalchemy import func
from api.group import listToString
from main import db
import datetime
from models import User, Group, Training


Days_and_numbers = {
    "Sunday": 6,
    "ראשון": 6,
    "Monday": 0,
    "שני": 0,
    "Tuesday": 1,
    "שלישי": 1,
    "Wednesday": 2,
    "רביעי": 2,
    "Thursday": 3,
    "חמישי": 3,
    "Friday": 4,
    "שישי": 4,
    "Saturday": 5,
    "שבת": 5
}


def id_in_group(group_ids, group_id):
    if group_ids == "":
        return False
    else:
        groups_list = group_ids.split(",")
    if str(group_id) in groups_list:
        return True
    return False


def list_intToString(lst):
    string_ints = [str(int) for int in lst]

    str_of_ints = ",".join(string_ints)
    return str_of_ints


def create_closest_training_for_each_group():
    groups_from_db = db.session.query(Group).all()
    for group in groups_from_db:
        day = group.day
        time = group.time
        trainging_date = datetime.date.today()
        while trainging_date.weekday() != Days_and_numbers[day]:
            trainging_date += datetime.timedelta(1)
        hour = time.split(':')
        trainging_date = datetime.datetime(trainging_date.year, trainging_date.month, trainging_date.day,
                                           int(hour[0]), int(hour[1]), 0)
        users_from_db = db.session.query(User).all()
        list_of_trainers = []
        list_of_users = []
        for user in users_from_db:
            if user.user_type in [2] and id_in_group(user.group_ids, group.id):
                list_of_trainers.append(user.id)
            if user.user_type in [3, 4] and id_in_group(user.group_ids, group.id):
                list_of_users.append(user.id)
        notes_dict = dict((el, 0) for el in list_of_users)
        new_training = Training(group_id=group.id, day=group_from_db.day,
                                time=group_from_db.time,
                                meeting_place=group.meeting_place,
                                attendance_users=list_intToString(list_of_users),
                                is_happened=True,
                                trainers_id=list_intToString(list_of_trainers),
                                notes=json.dumps(notes_dict))
        db.session.add(new_training)
        training_id = db.session.query(func.max(Training.id)).scalar()
        training_string = group.trainings_list
        if training_string == "" or training_string is None:
            training_list = []
        else:
            training_list = training_string.split(",")
        training_list.append(str(training_id))
        group.trainings_list = listToString(training_list)
        db.session.commit()


create_closest_training_for_each_group()