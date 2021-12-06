from flask import Blueprint, abort,jsonify, url_for, session
import flask

from Server.models import User
from Server.models import Group
from Server.utils import token_required, login_required


admin = Blueprint('admin', __name__)


@admin.put('/admin/status_user')
@token_required
def status_user(current_user): #disable or activate user
    from Server.main import db
    if current_user.user_type != 1:
        return jsonify({"success": False,
                        "message": "User cannot change user details, unless it is admin"}), 401

    try:
        data = flask.request.json
        user_id = int(data['user_id'])
        status = int(data['active_or_not'])
        user_from_db = db.session.query(User).filter_by(id=user_id).first()
        if not user_from_db:
            return jsonify({'success': False, 'message': 'No user found!'})
        user_from_db.active_or_not = status
        db.session.commit()
        return jsonify({"success": True,
                        "message": 'user: '+str(user_from_db.email)+' status was changed by user: '+str(current_user.email)+' successfully'}), 200
    except:
        return jsonify(
            {"success": False, "message": "Something went wrong1"}), 400


@admin.get('/admin/get_all_groups')
@token_required
def get_all_groups(current_user):
    from Server.main import db
    if current_user.user_type != 1:
        return jsonify({"success": False,
                        "message": "User cannot see all group, unless it is admin"}), 401
    try:
        all_groups=db.session.query(Group).all()
        if not all_groups:
            return jsonify({'success': False, 'message': 'No groups found!'})
        list_return =[group.to_dict() for group in all_groups]
        db.session.commit()
        return jsonify({'success': True, 'list of group': list_return}), 200
    except:
        return jsonify(
            {"success": False, "message": "Something went wrong"}), 400


@admin.get('/admin/get_all_trainers')
@token_required
def get_all_trainers(current_user):
    from Server.main import db
    if current_user.user_type != 1:
        return jsonify({"success": False,
                        "message": "User cannot see all group, unless it is admin"}), 401
    try:
        all_trainers = db.session.query(User).filter_by(user_type=2).all()
        if not all_trainers:
            return jsonify({'success': False, 'message': 'No trainers found!'})
        list_return = [user.to_dict() for user in all_trainers]
        db.session.commit()
        return jsonify({'success': True, 'list of trainers': list_return}), 200
    except:
        return jsonify(
            {"success": False, "message": "Something went wrong"}), 400


@admin.get('/admin/get_all_users')
@token_required
def get_all_users(current_user):
    from Server.main import db
    if current_user.user_type != 1:
        return jsonify({"success": False,
                        "message": "User cannot see all group, unless it is admin"}), 401

    try:
        all_users_3 = db.session.query(User).filter_by(user_type=3).all()
        all_users_4 = db.session.query(User).filter_by(user_type=4).all()
        all_users=all_users_3+all_users_4
        if not all_users:
            return jsonify({'success': False, 'message': 'No users found!'})
        list_return = [user.to_dict() for user in all_users]
        db.session.commit()
        return jsonify({'success': True, 'list of users': list_return}), 200
    except:
        return jsonify(
            {"success": False, "message": "Something went wrong"}), 400
