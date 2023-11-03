from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import *
from datetime import datetime
from sqlalchemy.exc import IntegrityError



student = Blueprint('student', __name__)



@student.route('/book-room/<int:room_id>', methods=['POST'])
@login_required
def book_room(room_id):
    room = Rooms.query.get(room_id)
    
    if room:
        if room.user_id:
            flash('This room is already booked!', category='error')
        else:
            room.user_id = current_user.id
            db.session.commit()
            flash('Room booked successfully!', category='success')
    else:
        flash('Room not found!', category='error')
    
    return redirect(url_for('views.student_page'))



@student.route('/cancel-booking/<int:room_id>', methods=['POST'])
@login_required
def cancel_booking(room_id):
    room = Rooms.query.get(room_id)
    
    if room:
        if room.user_id == current_user.id:
            room.user_id = None
            room.checkout = False
            db.session.commit()
            flash('Booking canceled successfully!', category='success')
        else:
            flash('This room was not booked by you!', category='error')
    else:
        flash('Room not found!', category='error')
    
    return redirect(url_for('views.student_page'))


@student.route('/checkout/<int:room_id>', methods=['POST'])
@login_required
def checkout(room_id):
    room = Rooms.query.get(room_id)
    
    if room and room.user_id == current_user.id:
        room.checkout = True  # Set checkout status to True
        db.session.commit()
        flash('You have successfully checked out of the room.', category='success')
    else:
        flash('You cannot check out of a room that you did not book.', category='error')
    
    return redirect(url_for('views.student_page'))
