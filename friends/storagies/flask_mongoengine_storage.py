from mongoengine import ReferenceField, CASCADE

from friends.storagies.mongoengine_storage import (
    BaseMongoengineStorage,
    MongoenginFriendsMixin,
    MongoengineFriendInvitationMixin,
    MongoengineFriendshipRequestMixin,
    MongoengineUserMixin,
)


class FlaskMongoengineStorage(BaseMongoengineStorage):
    user = None
    friendInvitation = None
    friendshipRequest = None
    friends = None


def init_friends(app, db, user_cls):
    User = user_cls

    class UserKlass(MongoengineUserMixin):
        @classmethod
        def user_model(cls):
            return User

    class FriendInvitation(MongoengineFriendInvitationMixin, db.Document):
        from_user = ReferenceField(
            User,
            required=True,
            reverse_delete_rule=CASCADE,
            unique_with="to_user_email",
        )

    class FriendshipRequest(MongoengineFriendshipRequestMixin, db.Document):
        from_user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
        to_user = ReferenceField(
            User, required=True, reverse_delete_rule=CASCADE, unique_with="from_user"
        )

    class Friends(MongoenginFriendsMixin, db.Document):
        user1 = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
        user2 = ReferenceField(
            User, required=True, reverse_delete_rule=CASCADE, unique_with="user1"
        )

    FlaskMongoengineStorage.user = UserKlass
    FlaskMongoengineStorage.friendInvitation = FriendInvitation
    FlaskMongoengineStorage.friendshipRequest = FriendshipRequest
    FlaskMongoengineStorage.friends = Friends
