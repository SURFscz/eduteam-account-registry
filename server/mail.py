from threading import Thread

from flask import current_app, render_template
from flask_mail import Message


def _send_async_email(ctx, msg, mail):
    with ctx:
        mail.send(msg)


def _open_mail_in_browser(html):
    import tempfile
    import webbrowser

    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name + ".html"

    f = open(path, "w")
    f.write(html)
    f.close()
    webbrowser.open("file://" + path)


def _do_send_mail(subject, recipients, template, context):
    recipients = recipients if isinstance(recipients, list) else list(
        map(lambda x: x.strip(), recipients.split(",")))

    mail_ctx = current_app.app_config.mail
    msg = Message(subject=subject,
                  sender=(mail_ctx.get("sender_name", "eduTEAMS"), mail_ctx.get("sender_email", "no-reply@eduteams.org")),
                  recipients=recipients)
    msg.html = render_template(f"{template}.html", **context)
    mail_in_browser_ = current_app.config["OPEN_MAIL_IN_BROWSER"]
    if not mail_in_browser_:
        mail = current_app.mail
        ctx = current_app.app_context()
        thr = Thread(target=_send_async_email, args=[ctx, msg, mail])
        thr.start()

    if mail_in_browser_:
        _open_mail_in_browser(msg.html)
    return msg.html


def mail_verify_mail(context, recipients):
    return _do_send_mail(
        subject=f"eduTEAMS email verification code",
        recipients=recipients,
        template="verify_mail",
        context=context
    )
