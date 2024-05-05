from flask import Flask
from website.controller import routes

app = Flask(__name__, template_folder='website/templates')
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,debug=True)