from flask import Blueprint, render_template, redirect, url_for, session
from .models import Event, Comment, Bookings
from .forms import CommentForm, BookingForm, EventForm, EditEventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from flask.helpers import flash

bp = Blueprint('event', __name__, url_prefix='/events')

# event page
@bp.route("/<id>")
def view(id):
    event = Event.query.filter_by(event_id=id).first()

    # if event id does not exist
    if event is None:
        return redirect("/404", code=302)

    # set up comment and booking forms
    comment_form = CommentForm()
    booking_form = BookingForm()

    # check the current user and make sure they are logged in
    if session.get('username') and current_user.is_authenticated:
        current_username = session["username"]
    else:
        current_username = ""

    # prevent access for other users when status is unpublished
    if event.event_status == "Unpublished" and current_username != event.event_author:
        flash("You do not have access to view this event")
        return redirect(url_for('main.index'))

    else:
        # render the page
        return render_template("events/view.html", event = event, id = id, commentForm = comment_form, bookingForm = booking_form, currentUsername = current_username)

# comment route for posting a comment
@bp.route('/<id>/comment', methods = ['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        # insert the comment into the db
        comment = Comment(comment_body=form.comment.data,
                          event_id=id,
                          comment_author=current_user.username)
        db.session.add(comment)
        db.session.commit()

        flash("Successfully posted comment")

    # return user back to event page
    return redirect(url_for('event.view', id=id))

# booking route for booking an event
@bp.route('/<id>/booking', methods = ['GET', 'POST'])
@login_required
def book(id):
    # create booking
    form = BookingForm()

    # get event from db
    selected_event = Event.query.filter_by(event_id=id).first()

    # when user confirms booking
    if form.validate_on_submit():
        # find all bookings for this event
        selected_booking_list = Bookings.query.filter_by(event_id=id)

        # calculate the booking count after this purchase
        booking_counter = 0
        for booking in selected_booking_list:
            booking_counter = booking_counter + booking.ticket_qty

        # add purchased amount to counter
        booking_total = booking_counter + form.ticket_qty.data

        # check if booking total exceeds
        if booking_total <= selected_event.ticket_max:
            # insert booking in to db
            booking = Bookings(
                ticket_qty=form.ticket_qty.data,
                event_id=id,
                booking_author=current_user.username)

            db.session.add(booking)
            db.session.commit()

            # change booking to sold out if the last ticket was purchased
            if booking_total >= selected_event.ticket_max:
                selected_event.event_status = "Sold Out"
                db.session.commit()

            # success
            flash("Your booking has been successfully placed!")
        else:
            # show error and show remaining supply
            flash(f"You can't order that many tickets: {selected_event.ticket_max - booking_counter} left")
    
    # render the page
    return redirect(url_for('event.view', id=id))

# create an event page
@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    form = EventForm()

    # if user presses create event
    if form.validate_on_submit():
        db_file_path=check_upload_file(form)

        # insert event into db
        event = Event(
            event_name=form.name.data, 
            event_desc=form.description.data, 
            event_image=db_file_path, 
            event_date=form.date.data.strftime("%d/%m/%Y"),
            event_time=form.time.data.strftime("%H:%M:%S"),  
            event_category=form.category.data, 
            event_artist=form.artist.data, 
            event_venue=form.venue.data, 
            ticket_max=form.ticket_max.data, 
            event_status=form.status.data, 
            event_author=current_user.username)
        db.session.add(event)
        db.session.commit()

        flash("Successfully created event")
        return redirect(url_for("event.create"))

    return render_template('events/create.html', form=form, type="create")

# upload file to server for create event page
def check_upload_file(form):
    filepath=form.image.data
    filename=filepath.filename
    BASE_PATH=os.path.dirname(__file__)
    upload_path=os.path.join(BASE_PATH, 'static/images', secure_filename(filename))
    db_upload_path='/static/images/' + secure_filename(filename)
    filepath.save(upload_path)
    return db_upload_path

# edit an event
@bp.route('/<id>/edit', methods = ['GET', 'POST'])
@login_required
def edit(id):
    selected_event = Event.query.filter_by(event_id=id).first()
    form = EditEventForm()

    if form.validate_on_submit():

        # check how many bookings, so max doesn't go lower than that amount
        selected_booking_list = Bookings.query.filter_by(event_id=id)
        booking_count = 0
        for booking in selected_booking_list:
            booking_count = booking_count + booking.ticket_qty
        if form.ticket_max.data < booking_count:
            flash(f"Cannot update ticket allowance to be less than the booked amount: {booking_count}")

        elif form.status.data == "Open" and booking_count <= form.ticket_max.data:
            flash(f"Cannot set event to \"Open\" due to the ticket allowance and booked amount: {booking_count}")

        else:
            # update old event information to new information
            selected_event.event_name=form.name.data
            selected_event.event_desc=form.description.data
            selected_event.event_date=form.date.data.strftime("%d/%m/%Y")
            selected_event.event_time=form.time.data.strftime("%H:%M:%S") 
            selected_event.event_category=form.category.data
            selected_event.event_artist=form.artist.data
            selected_event.event_venue=form.venue.data
            selected_event.ticket_max=form.ticket_max.data
            selected_event.event_status=form.status.data
            db.session.commit()
            flash("Successfully updated event")
            return redirect(url_for('event.view', id=id))

    # autofill in data for ease of editing
    form.name.data=selected_event.event_name
    form.description.data=selected_event.event_desc
    form.category.data=selected_event.event_category
    form.artist.data=selected_event.event_artist
    form.venue.data=selected_event.event_venue
    form.ticket_max.data=selected_event.ticket_max
    form.status.data=selected_event.event_status

    return render_template('events/create.html', form=form, type="edit")

# delete event
@bp.route('/<id>/delete', methods = ['GET', 'POST'])
@login_required
def delete(id):
    selected_event = Event.query.filter_by(event_id=id).first()

    # only delete if user is the author
    if session["username"] == selected_event.event_author:

        selected_comment_list = Comment.query.filter_by(event_id=id)
        selected_booking_list = Bookings.query.filter_by(event_id=id)

        # delete all comments relating to event (FK constraints)
        for comment in selected_comment_list:
            db.session.delete(comment)

        for booking in selected_booking_list:
            db.session.delete(booking)

        db.session.delete(selected_event)
        db.session.commit()
        flash("Successfully deleted event")
        return redirect(url_for('main.index'))
    else:
        flash("You don't have access to this event")
        return redirect(url_for('main.index'))