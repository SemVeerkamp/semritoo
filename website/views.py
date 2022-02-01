from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import *
from website import db

import requests
import json
from datetime import datetime
from datetime import timedelta

from website.get_startlist import get_startlist
from website.get_result import get_result
from website.tournament import year, tag

import ast
with open('dict.txt') as f:
    data = f.read()
odds_dict = ast.literal_eval(data)

views = Blueprint('views', __name__)

startlist, starttimes, events, scheduled_starttimes, scheduled_events = get_startlist(year, tag)
results, podium_pictures, result_times = get_result(year, tag)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    time_now = datetime.utcnow()
    time_now = time_now - timedelta(microseconds=time_now.microsecond)
    time_now = time_now + timedelta(hours=1)
    if request.method == 'POST':
        prediction = request.form.getlist("prediction")
        user = current_user
        event = str(prediction[0])
        if len(prediction) < 4:
            flash(
                'Je hebt niet het goede aantal vakjes geselecteerd. Selecteer de afstand (bovenste veld) '
                'en je drie schaatsers en probeer het opnieuw',
                category='error')
        elif len(prediction[0]) < 9:
            flash("Selecteer eerst de startlist_afstand (en je drie rijders) voordat je je voorspelling opslaat",
                  category='error')
        elif prediction[0][9] != "_":
            flash("Selecteer eerst de startlist_afstand (en je drie rijders) voordat je je voorspelling opslaat",
                  category='error')
        else:
            a = []
            for voorspelling in user.predictions:
                a.append(voorspelling.event)
            if event in a:
                flash(
                    "Voor deze afstand heb je al een voorspelling ingevuld. Als je je voorspelling wilt veranderen "
                    "verwijder dan eerste de oude voorspelling",
                    category="error")
            else:
                event = str(prediction[0])
                rider_one = str(prediction[1])
                rider_two = str(prediction[2])
                rider_three = str(prediction[3])

                new_prediction = Prediction(
                    event=event,
                    rider_one=rider_one,
                    rider_two=rider_two,
                    rider_three=rider_three,
                    user_name=current_user.name
                )
                db.session.add(new_prediction)
                db.session.commit()
                flash('Voorspelling toegevoegd', category='succes')

    return render_template("home.html",
                           startlist=startlist,
                           starttimes=starttimes,
                           user=current_user,
                           time_now=time_now,
                           events=events,
                           scheduled_events=scheduled_events,
                           scheduled_starttimes=scheduled_starttimes
                           )


@views.route('/resultaten', methods=['GET', 'POST'])
@login_required
def uitslagen():
    return render_template("uitslagen.html",
                           results=results,
                           podium_pictures=podium_pictures,
                           user=current_user,
                           result_times=result_times
                           )


@views.route('/voorspellingen', methods=['GET', 'POST'])
def voorspellingen():
    time_now = datetime.utcnow()
    time_now = time_now - timedelta(microseconds=time_now.microsecond)
    time_now = time_now + timedelta(hours=1)
    predictions = Prediction.query.order_by(Prediction.event).all()
    return render_template("voorspellingen.html",
                           startlist=startlist,
                           starttimes=starttimes,
                           time_now=time_now,
                           user=current_user,
                           predictions=predictions
                           )


@views.route('/stand', methods=['GET', 'POST'])
def stand():
    gold = 4
    silver = 2
    bronze = 1
    scores = {}
    scores_per_user = {}
    users = User.query.order_by(User.name).all()
    for user in users:
        scores[user.name] = 0
        scores_per_user[user.name] = {}
        for event in results:
            scores_per_user[user.name][event.partition('_')[2]] = 0
    predictions = Prediction.query.order_by(Prediction.event).all()
    for prediction in predictions:
        for event in results:
            if prediction.event == event:
                if prediction.rider_one == results[event][0] or prediction.rider_two == results[event][0] or \
                        prediction.rider_three == results[event][0]:
                    scores[prediction.user_name] += gold
                    scores_per_user[prediction.user_name][event.partition('_')[2]] += gold
                if prediction.rider_one == results[event][1] or prediction.rider_two == results[event][1] or \
                        prediction.rider_three == results[event][1]:
                    scores[prediction.user_name] += silver
                    scores_per_user[prediction.user_name][event.partition('_')[2]] += silver
                if prediction.rider_one == results[event][2] or prediction.rider_two == results[event][2] or \
                        prediction.rider_three == results[event][2]:
                    scores[prediction.user_name] += bronze
                    scores_per_user[prediction.user_name][event.partition('_')[2]] += bronze
    scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    users = list(scores_per_user.keys())
    events = list(scores_per_user.values())[0]

    return render_template("stand.html",
                           user=current_user,
                           scores=scores_sorted,
                           scores_per_user=scores_per_user,
                           users=users,
                           events=events,
                           scheduled_events=scheduled_events,
                           scheduled_starttimes=scheduled_starttimes
                           )


@views.route('/refresh_prediction', methods=['GET', 'POST'])
def refresh_predictions():
    startlist, starttimes, events, scheduled_starttimes, scheduled_events = get_startlist(year, tag)
    results, podium_pictures, result_times = get_result(year, tag)
    flash("De startlijsten, afstanden, starttijden en resultaten zijn opnieuw geladen", category="succes")
    return render_template("refresh_prediction.html",
                           startlist=startlist,
                           starttimes=starttimes,
                           results=results,
                           podium_pictures=podium_pictures,
                           user=current_user,
                           result_times=result_times,
                           scheduled_events=scheduled_events,
                           scheduled_starttimes=scheduled_starttimes
                           )


@views.route('/delete-prediction', methods=['POST'])
def delete_prediction():
    prediction = json.loads(request.data)
    predictionId = prediction['predictionId']
    prediction = Prediction.query.get(predictionId)
    if prediction:
        if prediction.user_name == current_user.name:
            db.session.delete(prediction)
            db.session.commit()

    return jsonify({})


@views.route('/spelregels', methods = ["GET", "POST"])
def spelregels():
    return render_template('/spelregels.html',
                           user=current_user
                           )


@views.route('/odds', methods=['GET', 'POST'])
def odds():
    return render_template("odds.html",
                           user=current_user,
                           odds_dict=odds_dict
                           )

# delete all the prediction from everybody (clean the database)
#    predictions = Prediction.query.order_by(Prediction.id).all()
#    print(predictions)
#    for prediction in predictions:
#        db.session.delete(prediction)
#        db.session.commit()
