from datetime import datetime, timedelta
from ...srcode.models import User, Post, PostLike
from .testconfigs import session


def test_create_post_instance(session):
     """Test Function for a OSt instance

     Args:
         session ([db session]): [ takes an instance of a db]
     """   
     u1 = User(username='john', password = 'pass1', email='john@example.com')
     u2 = User(username='susan', password = 'pass2', email='susan@example.com')
     u3 = User(username='mary', password = 'pass3', email='mary@example.com')
     u4 = User(username='david', password = 'pass4', email='david@example.com')
     session.add_all([u1, u2, u3, u4])
     session.commit()

     # create four posts
     now = datetime.utcnow()
     p1 = Post(tag = 'test1',content="post from john", author=u1,
     date_posted=now + timedelta(seconds=1))
     p2 = Post(tag = 'test 2', content="post from susan", author=u2,
          date_posted=now + timedelta(seconds=4))
     p3 = Post(tag = 'test 3', content="post from mary", author=u3,
               date_posted=now + timedelta(seconds=3))
     p4 = Post(tag = 'test4', content="post from david", author=u4,
               date_posted=now + timedelta(seconds=2))
     session.add_all([p1, p2, p3, p4])
     session.commit()

     assert p1.author.username == 'john'
     assert p2.author.username == 'susan'
     assert p3.author.username == 'mary'
     assert p4.author.username == 'david'

def test_post_follow_action(session):
     """Test Function for a Ability to receive posts from followed users

     Args:
         session ([db session]): [ takes an instance of a db]
     """   
     u1 = User(username='john', password = 'pass1', email='john@example.com')
     u2 = User(username='susan', password = 'pass2', email='susan@example.com')
     u3 = User(username='mary', password = 'pass3', email='mary@example.com')
     u4 = User(username='david', password = 'pass4', email='david@example.com')
     session.add_all([u1, u2, u3, u4])
     session.commit()
     # create four posts
     now = datetime.utcnow()
     p1 = Post(tag = 'test1',content="post from john", author=u1,
     date_posted=now + timedelta(seconds=1))
     p2 = Post(tag = 'test 2', content="post from susan", author=u2,
          date_posted=now + timedelta(seconds=4))
     p3 = Post(tag = 'test 3', content="post from mary", author=u3,
               date_posted=now + timedelta(seconds=3))
     p4 = Post(tag = 'test4', content="post from david", author=u4,
               date_posted=now + timedelta(seconds=2))
     session.add_all([p1, p2, p3, p4])

     u1.follow(u2)  # john follows susan
     u1.follow(u4)  # john follows david
     u2.follow(u3)  # susan follows mary
     u3.follow(u4)  # mary follows david
     session.commit()

     # check the followed posts of each user
     f1 = u1.followed_posts().count() == 2
     f2 = u2.followed_posts().all() == [p3]
     f3 = u3.followed_posts().all(). count() == 1
     #f4 = u4.followed_posts().all()

     


