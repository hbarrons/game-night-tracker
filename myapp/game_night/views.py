from flask import g, render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import GameNight
from myapp.game_night.forms import GameNightForm

game_night = Blueprint('game_night', __name__)

@game_night.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = GameNightForm()
    if form.validate_on_submit():
        game_night = GameNight(game=form.game.data, text=form.text.data, user_id=current_user.id)
        db.session.add(game_night)
        db.session.commit()
        flash('Game Night Info Saved')
        print('Game informaiton was saved')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@game_night.route('/<int:game_night_id>')
def game_night(game_night_id):
    game_night = GameNight.query.get_or_404(game_night_id) 
    return render_template('game_night.html', title=game_night.title, date=game_night.date, post=game_night)

@game_night.route('/<int:game_night_id>/update',methods=['GET','POST'])
@login_required
def update(game_night_id):
    game_night = GameNight.query.get_or_404(game_night_id)

    if game_night.author != current_user:
        abort(403)

    form = GameNightForm()

    if form.validate_on_submit():
        game_night.game = form.game.data
        game_night.text = form.text.data
        db.session.commit()
        flash('Game Information Updated')
        return redirect(url_for('game_night.game_night', game_night_id=game_night.id))

    elif request.method == 'GET':
        form.game.data = game_night.game
        form.text.data = game_night.text

    return render_template('create_post.html',title='Updating',form=form)


@game_night.route('/<int:game_night_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(game_night_id):

    game_night = GameNight.query.get_or_404(game_night_id)
    if game_night.author != current_user:
        abort(403)

    db.session.delete(game_night)
    db.session.commit()
    flash('Game Information Deleted')
    return redirect(url_for('core.index'))