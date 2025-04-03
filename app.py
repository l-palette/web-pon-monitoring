from flask import Flask, session,render_template, redirect, url_for, send_from_directory
from monitor.monitor import monitor_bp
from view.view import view_bp
from login.login import login_bp
from register.register import register_bp
from forum.forum import forum_bp
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5434/db_devices' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'pepsicola' 
db.init_app(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/logout')
def logout():
    session.pop('username', None)  
    return redirect(url_for('index'))

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

app.register_blueprint(monitor_bp, url_prefix='/monitor')
app.register_blueprint(view_bp, url_prefix='/view')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(forum_bp, url_prefix='/forum')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
