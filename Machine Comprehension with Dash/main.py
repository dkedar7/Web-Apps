import os

from flask import Flask, request, render_template
from model import *


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    context = request.form.get('context')
    query = request.form.get('query')

    return answer(context, query)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))