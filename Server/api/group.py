import flask
from flask import Blueprint, jsonify
from Server.utils import token_required
from Server.models import Group, User

group = Blueprint('group', __name__)



@group.post('/group')
@token_required
def post_group(current_user):
    from Server.main import db
    if current_user.user_type in [3, 4]:
        return jsonify({"success": False,
                        "message": "User cannot create new group, unless it is admin/trainer"}), 401

    try:
        data = flask.request.json
        new_group = Group(day=data['day'], time=data['time'], meeting_place=data['meeting_place'],
                          trainers_list=data['trainers_list'], active_or_not=True)
        db.session.add(new_group)
        db.session.commit()
        return jsonify({"success": True, "group": new_group.to_dict()})
    except:
        return jsonify({"success": False, "message": "Something went wrong"}), 400


@group.delete('/group/<group_id>/')
@token_required
def delete_group(current_user, group_id):
    from Server.main import db
    group_to_delete = db.session.query(Group).filter_by(id=group_id).first()
    if not group_to_delete:
        return jsonify({'success': False, 'message': 'No group found!'})
    if current_user.user_type != 1:
        return jsonify({"success": False,
                        "message": "User cannot delete groups, unless it is admin"}), 401
    db.session.delete(group_to_delete)
    db.session.commit()
    return jsonify({"success": True,
                    "message": "Group: " + group_id + " was deleted successfully"}), 200


@group.get('/group/<group_id>/')
@token_required
def get_group(current_user, group_id):
    from Server.main import db
    group_from_db = db.session.query(Group).filter_by(id=group_id).first()
    if not group_from_db:
        return jsonify({'success': False, 'message': 'No group found!'})
    if current_user.user_type in [3, 4]:
        return jsonify({"success": False,
                        "message": "User cannot view group details, unless it is admin/trainer"}), 401
    return jsonify({'success': True, 'user': group_from_db.to_dict()})


@group.put('/group/<group_id>/')
@token_required
def put_group(current_user, group_id):
    from Server.main import db
    group_from_db = db.session.query(Group).filter_by(id=group_id).first()
    if not group_from_db:
        return jsonify({'success': False, 'message': 'No group found!'})
    if current_user.user_type in [3, 4]:
        return jsonify({"success": False,
                        "message": "User cannot update group details, unless it is admin/trainer"}), 401
    data = flask.request.json
    try:
        for key in data.keys():
            if key == 'day':
                group_from_db.day = data['day']
            if key == 'time':
                group_from_db.time = data['time']
            if key == 'meeting_place':
                group_from_db.meeting_place = data['meeting_place']
            if key == 'trainers_list':
                group_from_db.trainers_list = data['trainers_list']
            if key == 'trainees_list':
                group_from_db.trainees_list = data['trainees_list']
            if key == 'volunteers_list':
                group_from_db.volunteers_list = data['volunteers_list']
            if key == 'trainings_list':
                group_from_db.trainings_list = data['trainings_list']
        db.session.commit()
        return jsonify({"success": True, "user": group_from_db.to_dict()})
    except:
        return jsonify({"success": False, "message": "Something went wrong"}), 400


@group.put('/delete_user_from_group/<group_id>/')
@token_required
def delete_user_from_group(current_user, user_id):
    return 1


@group.put('/add_user_to_group/<group_id>/')
@token_required
def add_user_to_group(current_user, group_id):
    from Server.main import db
    group_from_db = db.session.query(Group).filter_by(id=group_id).first()
    if not group_from_db:
        return jsonify({'success': False, 'message': 'No group found!'})
    if current_user.user_type in [3, 4]:
        return jsonify({"success": False,
                        "message": "User cannot add users to group details, unless it is admin/trainer"}), 401
    try:
        data = flask.request.json
        user_id = int(data['user'])
        user_from_db = db.session.query(User).filter_by(id=user_id).first()
        if not user_from_db:
            return jsonify({'success': False, 'message': 'No user found!'})
        groups_string = user_from_db.group_ids
        groups_list = groups_string.split(",")
        if str(group_id) in groups_list:
            return jsonify({'success': False, 'message': 'User is already part of the group!'}), 400
        groups_list.append(str(group_id))
        user_from_db.group_ids = str(groups_list)
        db.session.commit()
        return jsonify({"success": False, "message": "Group was updated successfully"}), 200
    except:
        return jsonify({"success": False, "message": "Something went wrong"}), 400


@group.get('/get_all_users_by_group/<group_id>/')
@token_required
def get_all_users_by_group(current_user, group_id):
    return 1


@group.get('/get_all_trainers_by_group/<group_id>/')
@token_required
def get_all_trainers_by_group(current_user, group_id):
    return 1


@group.get('/get_all_trainings_by_group/<group_id>/')
@token_required
def get_all_trainings_by_group(current_user, group_id):
    return 1
