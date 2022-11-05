from flask import Blueprint, render_template, session, redirect, request
from flask_login import login_fresh
from .models import Bookings, Event
from .forms import CategoryFilterForm

bp = Blueprint('main', __name__)


@bp.route('/', methods = ['GET', 'POST'])
def index():
    filter = CategoryFilterForm()

    if filter.validate_on_submit():
        if filter.category.data == "All":
            selected_events_list = Event.query.all()
        else:
            selected_events_list = Event.query.filter_by(event_category=filter.category.data)
    else:
        selected_events_list = Event.query.all()

    return render_template('index.html', logged_in=login_fresh(), events_list=selected_events_list, form=filter)

@bp.route('/404')
def not_found():
    return render_template('404.html', logged_in=login_fresh())

@bp.route('/history')
def history():
    if not login_fresh():
        return redirect("/login", code=302)
    else:
        bookings = Bookings.query.filter_by(booking_author=session["username"])
        events = Event.query.all()
        return render_template('history.html', logged_in=login_fresh(), bookings=bookings, events=events)

# Go to search page
@bp.route('/search')
def search():
    search_results = Event.query.filter(Event.event_name.ilike(f"%{request.args.get('searchString')}%"))
    return render_template('search.html', results=search_results, logged_in=login_fresh())
