from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json
from .models import Rooms



views = Blueprint('views', __name__)



@views.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher_page():
    rooms = Rooms.query.all()  # Fetch all rooms from the database
    return render_template('teacher.html', user=current_user, rooms=rooms)



@views.route('/student', methods=['GET', 'POST'])
@login_required
def student_page():
    rooms = Rooms.query.filter_by(user_id=None).all()  # Query rooms without a user_id (i.e., rooms that are not booked yet)
    booked_rooms = Rooms.query.filter_by(user_id=current_user.id).all()  # Fetch rooms booked by the current student
    checked_out_rooms = Rooms.query.filter_by(user_id=current_user.id, checkout=True).all()  # Query rooms that are checked out by the current student
    return render_template('student.html', user=current_user, rooms=rooms, booked_rooms=booked_rooms, checked_out_rooms=checked_out_rooms)




@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html', user=current_user)