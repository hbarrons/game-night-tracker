from flask import render_template, request, Blueprint
from myapp.models import GameNight

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    game_night = GameNight.query.order_by(GameNight.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', game_night=game_night)

@core.route('/info')
def info():
    return render_template('info.html')