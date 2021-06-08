from json.decoder import JSONDecodeError
from flask import flash, Markup, request, make_response, redirect
import os
import json

from flask.wrappers import Response
NOTIFILE = os.path.dirname(os.path.realpath(__file__)) + '/notifications.json'

with open(NOTIFILE, 'r') as fp:
    try:
        notif_storage: dict = json.load(fp)
    except JSONDecodeError:
        notif_storage: dict = {}


class Notification(object):
    valid_types = {'primary',
                   'secondary',
                   'success',
                   'danger',
                   'warning',
                   'info',
                   'light'}

    def __init__(self, message: str, type: str = None, title: str = None,
                 link: tuple[str, str] = None) -> None:
        """Constructor method
        """
        self.message = message
        self.type = type if type in self.valid_types else None
        self.title = title
        self.link = link
        self.id = self.save_to_file()

    def __repr__(self) -> str:
        """Representation method
        """
        return f'Notification("{self.message}", "{self.type}", "{self.title}", \
            {self.link})'

    def __call__(self, url: str) -> None:
        self.run(url)

    def run(self, url: str) -> Response:
        """Shows the notification and saves it into the browser's cookies.

        :param url: url to redirect to after the notification.
        :type url: str
        :return: Response
        :rtype: Response
        """
        self.flash_notif()

        resp = make_response(redirect(url))
        curr_not = self.get_notification_ids()
        curr_not.append(self.id)
        cookie_val = "|".join(curr_not)
        resp.set_cookie('notifications', value=cookie_val)
        return resp

    def create_flash_string(self) -> str:
        message = []
        if self.title:
            message.append(f'<strong>{self.title}</strong> ')
        message.append(self.message)
        if self.link:
            message.append(f' <a href="{self.link[1]}">{self.link[0]}</a>')
        message = Markup(str("".join(message)))
        return message

    def flash_notif(self) -> None:
        return flash(self.create_flash_string(), category=self.type)

    def save_to_file(self) -> int:
        global notif_storage
        try:
            last_id = list(notif_storage.keys())[-1]
        except IndexError:
            last_id = '0'
        new_id = str(int(last_id) + 1)
        contents = self.create_flash_string()
        if contents in notif_storage.values():
            return [k for k, v in notif_storage.items() if v == contents][0]
        notif_storage.update({
            new_id: contents
        })
        with open(NOTIFILE, 'w') as f:
            f.write(json.dumps(notif_storage))
            f.close()
        return new_id

    @classmethod
    def get_notifications(cls) -> list:
        cookies: str = request.cookies.get('notifications')
        cookies: list = cookies.split('|') if cookies is not None else []
        cookies: list = [notif_storage.get(x) for x in cookies]
        return cookies

    @classmethod
    def get_notification_ids(cls) -> list:
        cookies: str = request.cookies.get('notifications')
        cookies: list = cookies.split('|') if cookies is not None else []
        return cookies
