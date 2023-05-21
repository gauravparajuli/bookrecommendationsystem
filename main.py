from crypt import methods
from email.mime import image
from flask import Flask, render_template, request

import pickle

app = Flask(__name__)


@app.route('/')
def home():
    top50 = pickle.load(open('model/top50books.pkl', 'rb'))
    return render_template('index.html', title=top50['Book-Title'].to_list(), author=top50['Book-Author'].to_list(), image=top50['Image-URL-M'].to_list(), vote=top50['num_ratings'].to_list(), rating=[round(x, 1) for x in top50['avg_ratings'].to_list()])


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('recommendations.html')


if __name__ == '__main__':
    app.run(debug=True)
