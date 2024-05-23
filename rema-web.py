from flask import Flask, request, jsonify, render_template
from rema import Rema

app = Flask(__name__)

@app.route('/rema', methods=['GET', 'POST'])
def rema():
    if request.method == 'POST':
        user_input = request.form['user_input']
        output = Rema(query=user_input, mode="manual")
        
        return render_template('rema-main.html', user_input=user_input, output=output)
    return render_template('rema-main.html')

@app.route('/')
def index():
    return render_template('conversation-mode.html')


@app.route('/conversation', methods=['POST'])
def conversation():
    user_input = request.form['user_input']
    output = Rema(query=user_input, mode="conversation")
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)