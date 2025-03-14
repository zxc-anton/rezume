from flask import render_template
from main import app, db

@app.errorhandler(404)
def no_found_error(error):
    return render_template(r'errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template(r'errors/500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template(r'errors/403.html'), 403

@app.errorhandler(401)
def unauthorized(error):
    return render_template(r'errors/401.html'), 401