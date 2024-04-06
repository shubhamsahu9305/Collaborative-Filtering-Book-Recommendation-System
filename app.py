from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

popular_books = pd.read_pickle("popular_books.pkl")
popular_books['Avg_Rating'] = popular_books['Avg_Rating'].apply(lambda x: round(x,2))
popular_books = popular_books[:50]

pivot_df = pd.read_pickle("pivot_df.pkl")
books = pd.read_pickle("books.pkl")
similarity_scores = pd.read_pickle("similarity_scores.pkl")


@app.route('/')
def home():
    return render_template('index.html',
                           book_name=popular_books['Book-Title'].to_list(),
                           author=popular_books['Book-Author'].to_list(),
                           image=popular_books['Image-URL-M'].to_list(),
                           votes=popular_books['Num_Rating'].to_list(),
                           rating=popular_books['Avg_Rating'].to_list()
                           )


@app.route('/recommender')
def recommender_template():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommender():
    user_input = request.form.get('user_input')
    if user_input != "":
        try:
            index = np.where(pivot_df.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])),
                                   key=lambda x: x[1], reverse=True)[1:9]

            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == pivot_df.index[i[0]]]
                item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].to_list())
                item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list())
                item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list())

                data.append(item)

            return render_template('recommend.html', Book_Name= user_input, data=data)

        except Exception as e:
            return render_template('recommend.html',error=e)
    else:
        return render_template('recommend.html')


if __name__ == "__main__":
    app.run(debug=True)
