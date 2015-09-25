from flask import Flask, request
app = Flask(__name__)

# app.run(debug=True)
app.run(port=5001)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tala')
def hello_world_tala():
    print request.args['kala']
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
