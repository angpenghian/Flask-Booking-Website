from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import *
from datetime import datetime
from sqlalchemy.exc import IntegrityError



teacher = Blueprint('teacher', __name__)



@teacher.route('/create-room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        room_name = request.form.get('room_name')
        room_size = request.form.get('room_size')
        room_price = request.form.get('room_price')
        date_str = request.form.get('date')  # Assuming you have a date field in your form

        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        if not room_name or not room_size or not room_price or not date:
            flash('Please fill in all fields!', category='error')
        else:
            new_room = Rooms(
                date=date,
                room_name=room_name,
                room_size=room_size,
                room_price=room_price
            )
            try:
                db.session.add(new_room)
                db.session.commit()
                flash('Room created successfully!', category='success')
                return redirect(url_for('views.teacher_page'))
            except IntegrityError:
                db.session.rollback()
                flash('A room with the name already exists!', category='error')

    return redirect(url_for('views.teacher_page'))



@teacher.route('/edit-room/<int:room_id>', methods=['POST'])
@login_required
def edit_room(room_id):
    room = Rooms.query.get(room_id)
    if not room:
        flash('Room not found!', category='error')
        return redirect(url_for('views.teacher_page'))

    room_name = request.form.get('room_name')
    room_size = request.form.get('room_size')
    room_price = request.form.get('room_price')
    date_str = request.form.get('date')

    # Convert the date string to a datetime object
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Invalid date format!', category='error')
        return redirect(url_for('views.teacher_page'))

    room.room_name = room_name
    room.room_size = room_size
    room.room_price = room_price
    room.date = date

    db.session.commit()

    flash('Room updated successfully!', category='success')
    return redirect(url_for('views.teacher_page'))



@teacher.route('/delete-room/<int:room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    room_to_delete = Rooms.query.get(room_id)
    if room_to_delete:
        db.session.delete(room_to_delete)
        db.session.commit()
        flash('Room deleted successfully!', category='success')
    else:
        flash('Room not found!', category='error')
    return redirect(url_for('views.teacher_page'))