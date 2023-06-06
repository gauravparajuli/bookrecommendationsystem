from crypt import methods
from email.mime import image
import numpy as np
from flask import Flask, render_template, request

import pickle

app = Flask(__name__)

top50 = pickle.load(open('model/top50books.pkl', 'rb'))
pt = pickle.load(open('model/pt.pkl', 'rb'))
books = pickle.load(open('model/books.pkl', 'rb'))
similarity_score = pickle.load(open('model/similarity_score.pkl', 'rb'))


def recommend(bookname):

    return data


@app.route('/')
def home():

    return render_template('index.html', title=top50['Book-Title'].to_list(), author=top50['Book-Author'].to_list(), image=top50['Image-URL-M'].to_list(), vote=top50['num_ratings'].to_list(), rating=[round(x, 1) for x in top50['avg_ratings'].to_list()])


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('recommendations.html', bookname='')
    else:
        book = str(request.form['bookname'])

        # fetch book index
        index = np.where(pt.index == book)[0][0]
        similiar_items = sorted(
            list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:8]

        data = []
        for i in similiar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates(
                'Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render_template('recommendations.html', data=data, bookname=book)


if __name__ == '__main__':
    app.run(debug=True)
