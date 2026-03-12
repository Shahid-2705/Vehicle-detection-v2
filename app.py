from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Default routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # handle image upload (we'll do this later)
        pass
    return render_template('upload.html')

@app.route('/blacklist')
def blacklist():
    return render_template('blacklist.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
