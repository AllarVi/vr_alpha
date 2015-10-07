from flask import Flask, request, render_template, url_for, jsonify
import vra_resource
#import requests

app = Flask(__name__)


@app.route('/')
def index():
    # For testing purposes right now.
    return render_template('form_submit.html')

@app.route("/resourcereply", methods=['POST'])
def resourcereply():
    # This is to test the data that we got
    print("Data input to /resourcereply: " + str(request.get_data()))

    # string=request.form['yourstring']
    # return render_template('form_action.html', string=string)
    return jsonify(ip= '55.66.77.88',
                   port = '6788',
                   id = 'asasasas',
                   resource = '100')

@app.route('/resource', methods=['GET'])
def resource():
     # Read values from request.
     sendip = request.values.get('sendip')
     sendport = request.values.get('sendport')
     ttl = request.values.get('ttl')
     id = request.values.get('id')
     noask = request.values.getlist('noask')
     return vra_resource.resource_handler(sendip, sendport, ttl, id, noask)

@app.route('/checkmd5')
def checkmd5():
    return 'Hello World!'

@app.route('/answermd5')
def answermd5():
    return 'Hello World!'

if __name__ == '__main__':
    app.debug = True
    app.run()