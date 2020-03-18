from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/tovideo')
def tovideo() :
        return render_template('tovideo.html')


@app.route('/<_name>')
def hello(_name):
        return render_template('page.html', name=_name)


if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000')
