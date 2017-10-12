from mongoengine import ReferenceField

from friends.storagies.mongoengine_storage import BaseMongoengineStorage, MongoenginFriendsMixin, \
    MongoengineFriendInvitationMixin, MongoengineFriendshipRequestMixin, MongoengineUserMixin
from friends.utils import module_member


class FlaskMongoengineStorage(BaseMongoengineStorage):
    user = None
    friendInvitation = None
    friendshipRequest = None
    friends = None


def init_friends(app, db):
    if type(app.config['FRIENDS_USER_MODEL']) == str:
        User = module_member(app.config['FRIENDS_USER_MODEL'])
    else:
        User = app.config['FRIENDS_USER_MODEL']

    class UserKlass(User, MongoengineUserMixin):
        @classmethod
        def user_model(cls):
            return User

    class FriendInvitation(MongoengineFriendInvitationMixin):
        from_user = ReferenceField(User, required=True, unique_with='to_user_email')

    class FriendshipRequest(MongoengineFriendshipRequestMixin):
        from_user = ReferenceField(User, required=True)
        to_user = ReferenceField(User, required=True, unique_with='from_user')

    class Friends(MongoenginFriendsMixin):
        user1 = ReferenceField(User, required=True)
        user2 = ReferenceField(User, required=True, unique_with='user1')

    FlaskMongoengineStorage.user = UserKlass
    FlaskMongoengineStorage.friendInvitation = FriendInvitation
    FlaskMongoengineStorage.friendshipRequest = FriendshipRequest
    FlaskMongoengineStorage.friends = Friends
