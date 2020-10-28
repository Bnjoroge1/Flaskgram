from flask.globals import session
from ..srcode.models import User, Post, PostLike, Notification

def test_create_user_instance(session):
     """Test Function for a user instance

     Args:
         session ([db session]): [ takes an instance of a db]
     """     
     user1_test = {
          email :'test@example.com',
          username : 'test_user',
          password : 'foobarbaz',
     }
     user1_object = User(**user1_test)
     session.add(user1_object)
     session.commit()
     assert user1_object.id is not None
     assert user1_object.admin is False
     assert user1_object.confirmed is False
     assert user1_object.number_of_saved_posts.count() == 0
     assert user1_object.messages_sent.count() == 0
     assert user1_object.followed_posts.count() == 0
     assert user1_object.followers.count() == 0
     assert user1_object.followed.count() == 0

def test_follow_action(session):
     """Test Follow/Unfollow user relationship

     Args:
         session ([db session]): [ takes an instance of a db]
     """     
     user1_test = {
          email :'test1@example.com',
          username : 'test_user1',
          password : 'foobarbaz1',
     }
     user1_object = User(**user1_test)
     user2_test = {
          email :'test2@example.com',
          username : 'test_user2',
          password : 'foobarbaz2',
     }
     user2_object = User(**user2_test)
     session.add(user1_object)
     session.add(user2_object)
     session.commit()

     assert user1_object.followed.count() == 0
     assert user2_object.followed.count() == 0
     assert user1_object.followers.count() == 0
     assert user2_object.followers.count() == 0

     #*Follow
     user1_object.follow(user2_object)
     assert user1_object.is_following(user2_object) is True
     assert user2_object.followed.count()  == 1
     assert user2_object.is_following(user1_object) is False
     assert user1_object.followed.first().username == 'test_user2'
     assert user2_object.followers.first().username == 'test_user1'

     #!unfollow
     user1_object.unfollow(user2_object)
     assert user1_object.is_following(user2_object) is False
     assert user1_object.followed.count() == 0


     
