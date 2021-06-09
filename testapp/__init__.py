from flask import Flask, render_template, url_for, request, Markup, make_response
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Regexp
from FlashNotifsStorage import Notification
from random import choice


def make_app():
    app = Flask(__name__)
    app.secret_key = "2f13647db31cb8d13e0a515f8a07dee7"

    class Cookie(FlaskForm):
        captcha = StringField('Please enter "spain" here.', validators=[
            Regexp('spain'), DataRequired()])
        submit = SubmitField('Get one free!')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = Cookie()
        if form.validate_on_submit():
            n = choice([
                Notification(
                    'One cookie has been added to your inventory!', 'success'),
                Notification(
                    'You have consumed too much cookies.', 'error'),
                Notification(
                    'Jar almost empty', 'warning', 'Attention!.'),
                Notification(
                    '1 cookie added to your inventory!', 'primary'),
                Notification(
                    '2 cookies added to your inventory!', 'secondary'),
            ])
            n('/')

            resp = make_response(render_template('index.html', form=form))
            curr_not = n.get_notification_ids()
            curr_not.append(n.id)
            cookie_val = "|".join(curr_not)
            resp.set_cookie('notifications', value=cookie_val)
            return resp
        return render_template('index.html', form=form)

    @app.context_processor
    def notif_handler():
        notifications = Notification.get_notifications()
        n_count = len(notifications)
        return dict(notifications=notifications, n_count=n_count)

    return app
