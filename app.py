from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'سلام دنیا! این اولین پروژه Flask منه!'

if __name__ == '__main__':
    app.run(debug=True)
