from data import data_manager
from psycopg2.extensions import AsIs


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_highest_rated_shows(page, sort_method, sort_direction):
    query = """
    SELECT shows.id, shows.title as title, year, runtime, ROUND(rating, 1) as rating, subquery.genres as genres,
    trailer, homepage from 
    (SELECT shows.title as title, string_agg(genres.name, ', ') as genres from genres
    JOIN show_genres on genres.id = show_genres.genre_id
    JOIN shows on show_genres.show_id = shows.id
    GROUP BY shows.title) AS subquery
    JOIN shows on shows.title = subquery.title
    ORDER BY %(sort_method)s %(sort_direction)s
    LIMIT 15
    OFFSET (%(page)s - 1) * 15
    """
    data = {'page': page, 'sort_method': AsIs(sort_method), 'sort_direction': AsIs(sort_direction)}
    return data_manager.execute_select(query, data)


def get_shows_page_count():
    query = """SELECT count(*) / 15 as count from shows"""
    result = data_manager.execute_select(query)
    return result[0]['count']


def get_show_details(show_id):
    query1 = """
    SELECT title, runtime, ROUND(rating, 1) as rating, overview, year, trailer from shows
    where id = %(show_id)s"""

    query2 = """
    SELECT string_agg(genres.name, ', ') as genres from genres
    join show_genres on show_genres.genre_id = genres.id
    WHERE show_genres.show_id = %(show_id)s
    group by show_genres.show_id"""

    query3 = """
    SELECT array_agg(actors.name) as actors, array_agg(actors.id) as actor_ids from show_characters
    join actors on show_characters.actor_id = actors.id
    WHERE show_characters.show_id = %(show_id)s
    group by show_characters.show_id"""

    data = {'show_id': show_id}

    show_details = dict(data_manager.execute_select(query1, data)[0])
    show_details['genres'] = data_manager.execute_select(query2, data)[0]['genres']
    show_details['actors'] = data_manager.execute_select(query3, data)[0]['actors']
    show_details['actor_ids'] = data_manager.execute_select(query3, data)[0]['actor_ids']
    return show_details


def get_actor_id_by_name(name):
    query = """
    SELECT id from actors
    WHERE name = %(name)s"""
    data = {'name': name}
    return data_manager.execute_select(query, data)[0]['id']


def get_actor_details(actor_id):
    query = """
    SELECT actors.name, actors.birthday, actors.death, actors.biography from actors
    where actors.id = %(actor_id)s;"""
    data = {'actor_id': actor_id}
    return data_manager.execute_select(query, data)


def get_actor_shows(actor_id):
    query = """SELECT character_name, s.title from show_characters
    left join shows s on show_characters.show_id = s.id
    where actor_id = %(actor_id)s;"""
    data = {'actor_id': actor_id}
    return data_manager.execute_select(query, data)


def get_100_actors_sorted_by_birth_date():
    query = """
    SELECT LEFT(name, POSITION(' ' IN name)) as first_name, id, birthday from actors
    ORDER BY birthday
    LIMIT 100;
    """
    return data_manager.execute_select(query)


def get_seasons(show_id):
    query = """
    SELECT season_number, title, overview from seasons
    where show_id = %(show_id)s"""
    data = {'show_id': show_id}
    return data_manager.execute_select(query, data)


def get_shows_by_actors_count():
    query = """
    select shows.title as title, (rating - (select avg(rating) from shows)) as rating_minus_avg, count(actors.id) as actors_count
    from shows
    left join show_characters on shows.id = show_characters.show_id 
    left join actors on show_characters.actor_id = actors.id
    group by shows.id
    order by actors_count DESC
    limit 10;"""
    return data_manager.execute_select(query)


def get_shows_by_episode_count(sort_method):
    query = """
    select shows.title, round(shows.rating) as rating, episode_count.episode_count as episode_count from shows
    left join (select count(episodes.id) as episode_count, seasons.show_id as show_id 
               from episodes 
               left join seasons on episodes.season_id = seasons.id
               group by seasons.show_id) as episode_count on episode_count.show_id = shows.id
    order by episode_count %(sort_method)s
    limit 10;"""
    data = {'sort_method': AsIs(sort_method)}
    return data_manager.execute_select(query, data)


def get_all_genres():
    query = """select name, id from genres"""
    return data_manager.execute_select(query)


def get_actors_by_search_params(genre, name):
    query = """select distinct a.name from genres g
    left join show_genres sg on g.id = sg.genre_id
    left join shows s on s.id = sg.show_id
    left join show_characters sc on sg.show_id = sc.show_id
    left join actors a on a.id = sc.actor_id
    where g.name = %(genre)s and lower(a.name) like %(name)s
    limit 20;"""
    data = {"genre": genre, 'name': name + '%'}
    return data_manager.execute_select(query, data)


def get_actors_by_birthday():
    query = """
    select name, birthday from actors
    order by birthday
    limit 100;"""
    return data_manager.execute_select(query)


def get_genre_data(genre_id):
    query = """
    select shows.title, count(actors.id) as actors_count, shows.rating, shows.year from show_genres
    left join shows on show_genres.show_id = shows.id
    left join show_characters on shows.id = show_characters.show_id
    left join actors on show_characters.actor_id = actors.id
    where show_genres.genre_id = %(genre_id)s 
    group by shows.id
    having count(actors.id) < 20"""
    data = {'genre_id': genre_id}

    return data_manager.execute_select(query, data)
