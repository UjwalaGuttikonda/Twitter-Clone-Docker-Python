from operator import attrgetter
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    search_results = []
    no_results_found = False
    followed_tweets = []

    if request.method == 'POST':
        # Check for form actions
        if 'user_follow' in request.form:
            # Follow user action
            followed_user = request.form.get('user_follow')
            user_to_follow = User.query.filter_by(email=followed_user).first()

            if user_to_follow:
                if user_to_follow == current_user:
                    flash("You cannot follow yourself!", category='error')
                else:
                    current_user.followed_users.append(user_to_follow)
                    db.session.commit()
                    flash(f"You are now following {user_to_follow.email}!", category='success')
            else:
                flash("User not found.", category='error')
            return redirect(url_for('views.home'))


        elif 'note' in request.form:
            # Add note action
            note = request.form.get('note')

            if len(note) < 1:
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
            return redirect(url_for('views.home'))

        elif 'retweet' in request.form:
            # Retweet action
            retweet_id = request.form.get('retweet')
            retweet_note = Note.query.get(retweet_id)

            if retweet_note:
                if retweet_note in current_user.retweeted_notes:
                    flash('You have already retweeted this tweet.', category='error')
                else:
                    current_user.retweeted_notes.append(retweet_note)
                    db.session.commit()
                    flash('Tweet retweeted!', category='success')
            else:
                flash('Tweet not found.', category='error')
            return redirect(url_for('views.home'))

        elif 'search_tweet' in request.form:
            # Search action
            search_query = request.form.get('search_tweet')
            search_results = Note.query.filter(Note.data.contains(search_query)).all()
            no_results_found = len(search_results) == 0
            #return redirect(url_for('views.home'))

    followed_users = current_user.followed_users.all()
    for user in followed_users:
        followed_tweets.extend(user.notes)
        
    followed_tweets.sort(key=lambda x: x.date, reverse=True) 
    
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()

    print("Context:", locals())  # Print the context variables
    print("User:", current_user)  # Print the current user
    print("User Username:", current_user.username)  # Print the current user's username
    retweeted_notes = current_user.retweeted_notes

    return render_template("home.html", user=current_user, search_results=search_results, no_results_found=no_results_found, followed_tweets=followed_tweets, retweeted_notes=retweeted_notes)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# Other routes and views...
