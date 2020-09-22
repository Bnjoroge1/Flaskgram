import secrets, os, flask_s3
from config import Config
from werkzeug.utils import  secure_filename
import boto3

def save_async_picture(app, s3_send):
    '''FUcntionality to send emails asynchronously in the background, accepts both the meessage and the instance of the flask app.
     Giving flask mail a context of our app so that it can access config values'''
    with app.app_context():
        s3_send()
def save_picture(form_picture, type):
    '''FUcntion to upload modified static files to an s3 bucket'''
    '''create a filename using a random hex'''
   

    random_hex = secrets.token_hex(5)
    _,file_ext = os.path.splitext(form_picture.filename)
    #f_name = form_picture.filename
    picture_fn = random_hex + file_ext  
    
    s3_client = boto3.client(
        's3',
        region_name = Config.S3_LOCATION,
        endpoint_url = f'https://{Config.AWS_BUCKET}.s3.amazonaws.com/profile_pics',
        aws_access_key_id = Config.AWS_ACCESS_KEY,
        aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY
    )
    try:
           
        filename = secure_filename(picture_fn)
        if type =='profile':
            bucket = 'Profile_pics'

        elif type == 'post':
            bucket = 'Post'
        s3_client.put_object(
            ACL = 'public-read',
            Bucket = bucket,
            Key = filename,
            Body = form_picture,
            ContentType = form_picture.content_type
        )
        
    except Exception as e:
        raise e
        print('Something happened with the upload', 'danger')
  
    return picture_fn 