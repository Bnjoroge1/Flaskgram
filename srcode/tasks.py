from flask import render_template
from config import EmailConfig
from .user.email import send_posts
import time, sys, json
from rq import get_current_job
from . import create_current_app
from .models import Post, User, db, Task

app = create_current_app()
app.app_context().push()

def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i /seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')

def _set_task_progress(progress):
    """Sets the task's progress in percentage

    Args:
        progress ([progress]): [percent]
    """    
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()
    
def export_tasks(user_id):
    try:
        #Read users posts from the database  and organize the posts received into a list of dictionaries,
        user = User.query.get(id=user_id)
        _set_task_progress(0)
        posts_data = []
        i = 0
        number_posts = user.posts.count()
        for post in user.posts.order_by(Post.date_posted.asc()):
            posts_data.append(
                {
                    'body': post.content,
                    'timestamp': post.date_posted.strftime('%a,%b,%Y')
                }
            )
            time.sleep(5)
            i =+ 1
            _set_task_progress(100*i // number_posts)

        #email the posts as a background job. 
        send_posts(
            f'[Flaskgram] {user.username}Your Posts', sender= EmailConfig.DEFAULT_MAIL_SENDER, recipients= [user.email], html_body= render_template('user/export_posts.html'),body_html= render_template('user/export_posts.txt'), attachments=[('posts.json', 'application/json', 
            json.dumps({'posts': posts_data}, indent= 4))], sync=True)
    except:
        #flask typically catches exceptions and displays them depending on the logging configuration implemented by me. However, since we are creating a new application specific to this rq client, we are going to implement a custom error handler informing you that the error has not been logged.
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        #Set the task rprogress as 'complete'
        _set_task_progress(100)