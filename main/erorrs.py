from flask import render_template
from main import application 

@application.errorhandler(404)
def no_found_error(error):
    return render_template(r'errors/404.html'), 404

@application.errorhandler(500)
def internal_server_error(error):
    return render_template(r'errors/500.html'), 500

@application.errorhandler(403)
def forbidden(error):
    return render_template(r'errors/403.html'), 403

@application.errorhandler(401)
def unauthorized(error):
    return render_template(r'errors/401.html'), 401