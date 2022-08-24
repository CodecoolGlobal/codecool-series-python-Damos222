from flask import Flask, render_template, url_for, redirect, jsonify, request
from data import queries
import math
from dotenv import load_dotenv

load_dotenv()
app = Flask('codecool_series')

@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('new-index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows')
def shows():
    return redirect('/shows/most-rated/1/rating/desc')


@app.route('/shows/most-rated/')
def most_rated():
    return redirect('/shows/most-rated/1/rating/desc')


@app.route('/shows/most-rated/<int:page>/<sort_method>/<sort_direction>')
def sortable_shows_table(page, sort_method, sort_direction):
    shows = queries.get_highest_rated_shows(page, sort_method, sort_direction)
    page_count = queries.get_shows_page_count()
    return render_template('shows.html', shows=shows, page=page, page_count=page_count,
                           sort_method=sort_method, sort_direction=sort_direction)


@app.route('/show/<int:show_id>')
def show_details(show_id):
    show = queries.get_show_details(show_id)
    if show["runtime"] > 60:
        show["runtime"] = f'{show["runtime"] // 60}:{show["runtime"] % 60} h'
    else:
        show["runtime"] = f'{show["runtime"]} min'
    actors_count = len(show['actors']) if len(show['actors']) < 3 else 3
    seasons = queries.get_seasons(show_id)
    return render_template('show-details.html', show=show, actors_count=actors_count, seasons=seasons)


@app.route('/actors/<int:actor_id>')
def get_shows_by_actor(actor_id):
    actor_shows = queries.get_actor_shows(actor_id)
    return jsonify(actor_shows)


@app.route('/ratings')
def ratings_page():
    shows = queries.get_shows_by_actors_count()
    return render_template('ratings.html', shows=shows)


@app.route('/actors')
def all_actors():
    actors = queries.get_100_actors_sorted_by_birth_date()
    return render_template('actors.html', actors=actors)


@app.route('/ordered-shows')
def add_sort_parameter():
    return redirect('/ordered-shows/desc')


@app.route('/ordered-shows/<sort_method>')
def ordered_shows(sort_method):
    if sort_method == '':
        sort_method = 'desc'
    shows = queries.get_shows_by_episode_count(sort_method)
    for show in shows:
        show['rating'] = int(show['rating'])
    return render_template('ordered-shows.html', shows=shows, sort_method=sort_method)


@app.route('/filter-actors')
def filter_actors():
    genres = queries.get_all_genres()
    return render_template('filter-actors.html', genres=genres)


@app.route('/api/filter-actors', methods=['POST'])
def get_actors_by_search_params():
    genre = request.form.get('genre')
    name = request.form.get('name')
    print(genre, name)
    actors = queries.get_actors_by_search_params(genre, name)
    return jsonify(actors)


@app.route('/birthday-actors')
def actors_by_birthday():
    actors = queries.get_actors_by_birthday()
    for actor in actors:
        actor['birthday_day'] = actor['birthday'].day
    return render_template('birthday-actors.html', actors=actors)


@app.route('/genres')
def genres():
    genres = queries.get_all_genres()
    return render_template('genres.html', genres=genres)


@app.route('/api/genre/<genre_id>')
def get_genres_data(genre_id):
    data = queries.get_genre_data(genre_id)
    return jsonify(data)


@app.route('/most-common-character-names')
def most_common_character_names():
    character_names = queries.get_most_common_character_names()
    return render_template('most-common-character-names.html', character_names=character_names)


@app.route('/shows-with-5-or-more-genres')
def shows_with_5_or_more_genres():
    shows = queries.get_shows_with_5_or_more_genres()
    return render_template('shows-with-5-or-more-genres.html', shows=shows)


@app.route('/api/shows-with-5-or-more-genres/<int:show_id>')
def get_shows_with_5_or_more_genres_details(show_id):
    show_info = queries.get_show_info(show_id)
    return jsonify(show_info)



def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
