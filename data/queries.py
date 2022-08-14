from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


# def get_highest_rated_shows():
#     query = """SELECT title, year, runtime, ROUND(rating, 1) as rating, string_agg(genres.name, ', ') as genres, trailer, homepage from genres
#     JOIN show_genres on genres.id = show_genres.genre_id
#     JOIN shows on show_genres.show_id = shows.id
#     GROUP BY shows.title
#     ORDER BY rating DESC
#     LIMIT 15
#     """
#     return data_manager.execute_select(query)


def get_highest_rated_shows(page):
    query = """SELECT shows.id, shows.title, year, runtime, ROUND(rating, 1) as rating, subquery.genres, trailer, homepage from 
    (SELECT shows.title as title, string_agg(genres.name, ', ') as genres from genres
    JOIN show_genres on genres.id = show_genres.genre_id
    JOIN shows on show_genres.show_id = shows.id
    GROUP BY shows.title) AS subquery
    JOIN shows on shows.title = subquery.title
    ORDER BY rating DESC
    LIMIT 15
    OFFSET (%(page)s - 1) * 15
    """
    data = {'page': page}
    return data_manager.execute_select(query, data)


def get_shows_page_count():
    query = """SELECT count(*) / 15 as count from shows"""
    result = data_manager.execute_select(query)
    return result[0]['count']


# def get_genres_of_show(show_id):
#     query = '''SELECT genres.name from show_genres
#     JOIN genres on show_genres.genre_id = genres.id
#     WHERE show_genres.show_id = %(show_id)s'''
#     data = {'show_id': show_id}
#     data_manager.execute_select(query, data)
