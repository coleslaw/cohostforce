from django.core.management.base import BaseCommand
from online_site.models import Profile , ContestResult
from online_site.documents import ProfileDocument, ContestResultDocument
from elasticsearch_dsl import Document, Integer, Text, Object
import glob
import pandas as pd
import os
from elasticsearch_dsl.connections import connections


def get_user(username):
    return Profile.objects.get(name=username)

def get_file_name(file_path):
    cur_file = os.path.basename(file_path)
    username = os.path.splitext(cur_file)[0] 
    return username

def get_rating(file_data):
    return file_data['New rating'].iloc[len(file_data) - 1]    

def get_max_rating_title(file_data):
    max_rating = 0
    best_title = 'something'
    for i in range( len(file_data) ):
        if int(file_data['New rating'].iloc[i] ) > max_rating:
            max_rating = int(file_data['New rating'].iloc[i] )
            best_title = file_data['Title'].iloc[i]
    return (max_rating, best_title)

def get_title(file_data):
    return file_data['Title'].iloc[ len(file_data) - 1 ]

def get_contests( new_user, file_data ):
    contests = []
    for i in range( len(file_data) ):
        new_contest_result = ContestResult()
        new_contest_result.name = file_data['Contest'][i]
        new_contest_result.rating_change = file_data['Rating change'][i]
        new_contest_result.new_rating = file_data['New rating'][i]
        new_contest_result.title_change = file_data['Title']
        new_contest_result.user = get_user(new_user)
        contests.append(new_contest_result)
    return contests

def is_exist_profile(username):
    try:
        Profile.objects.get(name=username)
        return True
    except:
        return False

def is_exist_contest_results(username, contest_name):
    user = get_user(username)
    try:
        ContestResult.objects.get(name=contest_name, user=user)
        return True
    except:
        return False

def add_profiles(all_files):
    connections.create_connection(
        hosts=['https://elastic:xhBqmy8XqOYQSZYjspBVsnPK@daa681.es.us-east-1.aws.found.io']
    )
    cnt = 0
    for file_path in all_files:
        name = get_file_name(file_path)
        file_data = pd.read_csv(file_path, index_col=0)
        rating = get_rating(file_data)
        max_rating, best_title = get_max_rating_title(file_data)
        title = get_title(file_data)
        ''' if is_exist_profile(name) == False:
        new_profile = Profile(
            name=name,
            rating=rating,
            max_rating=max_rating,
            best_title=best_title,
            title=title
        )
        #new_profile.save()
        #save vao db.sqlite3 '''

        profile_dict = ProfileDocument()
        profile_dict.name = name
        profile_dict.rating = rating
        profile_dict.max_rating = max_rating
        profile_dict.best_title = best_title
        profile_dict.title = title
        profile_dict.save()
        #  cnt+=1
        #  print(str(profile_dict),cnt)
        '''profile_doc = ProfileDocument(**profile_dict)
        print(profile_doc)
        print(profile_dict)'''

        # save vao elasticsearch


def add_contest_results(all_files):
    connections.create_connection(
        hosts=['https://elastic:xhBqmy8XqOYQSZYjspBVsnPK@daa681.es.us-east-1.aws.found.io']
    )
    for file_path in all_files:
        username = get_file_name(file_path)
        '''user = get_user(username)'''
        file_data = pd.read_csv(file_path, index_col=0)
        for i in range( len(file_data) ):
            contest_name = file_data['Contest'].iloc[i]
            rating_change = file_data['Rating change'].iloc[i]
            new_rating = file_data['New rating'].iloc[i]
            title_change = file_data['Title'].iloc[i]
            '''
            if is_exist_contest_results(username, file_data['Contest'].iloc[i]) :
                continue 
            new_contest_result = ContestResult(
                name = contest_name,
                rating_change = rating_change,
                new_rating = new_rating,
                title_change = title_change,
                user = user
            )
            new_contest_result.save()'''
            contest_result_dict = ContestResultDocument()
            contest_result_dict.name = contest_name
            contest_result_dict.rating_change = rating_change
            contest_result_dict.new_rating = new_rating
            contest_result_dict.title_change = title_change
            contest_result_dict.user = {
                    'name': username
                }
            contest_result_dict.save()


class Command(BaseCommand):
    help = 'Load csv files into models'

    def add_arguments(self, parser):
        parser.add_argument('csv_dir', help="Directory containing CSV files")
    
    def handle(self, *args, **options):
        csv_dir = options['csv_dir']
        all_files = glob.glob(csv_dir + '/*.csv')
        add_profiles(all_files)
        add_contest_results(all_files)





            