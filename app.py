from flask import Flask
from flask import make_response

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

# /recommendation/api/v1.0/location
@app.route('/recommendation/api/v1.0/rec',methods=['GET'])
def get_recommendations()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




if __name__ == "__main__":
    app.run(debug=True)
    # app.run()