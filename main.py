from flask import Flask, render_template, url_for
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/most-rated/<int:page>')
def most_rated(page):
    shows = queries.get_highest_rated_shows(page)
    page_count = queries.get_shows_page_count()
    return render_template('highest-rated.html', shows=shows, page=page, page_count=page_count)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
