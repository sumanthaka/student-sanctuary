from flask import render_template


def page_not_found(e):
    return render_template('error/404.html'), 404

def page_forbidden(e):
    return render_template('error/403.html'), 403