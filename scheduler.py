# scheduler.py

from celery import Celery
from celery.schedules import crontab
from data_collection import fetch_top_repos
from data_storage import insert_repos
from data_processing import load_model, categorize_repo

app = Celery('tasks', broker='redis://localhost:6379')

app.conf.beat_schedule = {
    'update-repo-data-daily': {
        'task': 'scheduler.update_repo_data',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}

@app.task
def update_repo_data():
    repos = fetch_top_repos()
    insert_repos(repos)
    
    # Categorize repos
    model = load_model()
    for repo in repos:
        category = categorize_repo(model, repo['description'], repo.get('topics', []))
        # TODO: Update repo category in database

if __name__ == '__main__':
    app.start()