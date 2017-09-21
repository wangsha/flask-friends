from datetime import datetime

from mongoengine import EmailField, StringField, DateTimeField, Q

from friends.storage import UserMixin, FriendInvitationMixin, FriendshipRequestMixin, FriendsMixin, \
    BaseStorage


class MongoengineUserMixin(UserMixin):
    @classmethod
    def user_exists(cls, email):
        """
        Return True/False if a User instance exists with the given email.
        """
        flt = dict()
        flt[cls.username_field()] = email
        return cls.user_model().objects.filter(**flt).count() > 0

    @classmethod
    def get_users_by_email(cls, email):
        """Return users instance for given email address"""
        flt = dict()
        flt[cls.username_field()] = email
        return cls.user_model().objects.filter(**flt)


class MongoengineFriendInvitationMixin(FriendInvitationMixin):
    from_user = None
    to_user_email = EmailField(max_length=255, required=True)
    message = StringField(max_length=140)

    @classmethod
    def create(cls, from_user, to_user_email, message):
        return cls.objects(
            from_user=from_user,
            to_user_email=to_user_email
        ).upsert_one(
            set__message=message,
        )

    @classmethod
    def get_invitations_by_email(cls, to_user_email):
        return cls.objects.filter(to_user_email=to_user_email)

    @classmethod
    def remove(cls, ids_to_delete):
        cls.objects.filter(pk__in=ids_to_delete).delete()


class MongoengineFriendshipRequestMixin(FriendshipRequestMixin):
    from_user = None
    to_user = None
    message = StringField(max_length=140)
    rejected_at = DateTimeField()

    @classmethod
    def create(cls, from_user, to_user, message=None):
        """Create a friendship request"""
        #TODO: handle existing to_user friend from_user
        obj = cls.objects(from_user=from_user, to_user=to_user)\
            .upsert_one(set__message=message)

    @classmethod
    def get_request(cls, from_user, to_user):
        """Return a non-rejected friendship request"""
        return cls.objects(from_user=from_user, to_user=to_user, rejected_at=None)

    @classmethod
    def get_request_by_from_user(cls, from_user):
        """Return non-rejected friendship requests initiated by given from_user"""
        return cls.objects(from_user=from_user, rejected_at=None)

    @classmethod
    def get_request_by_to_user(cls, to_user):
        """Return non-rejected friendship requests made to given to_user"""
        return cls.objects(to_user=to_user, rejected_at=None)

    @classmethod
    def get_rejected_request_by_from_user(cls, from_user):
        """Return rejected friendship requests initiated by given from_user"""
        return cls.objects(from_user=from_user, rejected_at__neq=None)

    @classmethod
    def get_rejected_request_by_to_user(cls, to_user):
        """Return rejected friendship requests made to given to_user"""
        return cls.objects(to_user=to_user, rejected_at__neq=None)

    @classmethod
    def remove(cls, ids_to_delete):
        return cls.objects.filter(pk__in=ids_to_delete).delete()

    @classmethod
    def reject(cls, ids_to_reject):
        return cls.objects.filter(pk__in=ids_to_reject).update(set__rejected_at=datetime.utcnow())


class MongoenginFriendsMixin(FriendsMixin):
    user1 = None
    user2 = None

    @classmethod
    def create(cls, user1, user2):
        query1 = Q(user1=user1, user2=user2)
        query2 = Q(user1=user2, user2=user1)
        obj = cls.objects.filter(query1 or query2).first()
        if not obj:
            obj = cls(user1=user1, user2=user2)
            obj.save()

        return obj

    @classmethod
    def get_friends(cls, user):
        res = cls.objects.filter(Q(user1=user) or Q(user2=user)).first()
        return res

    @classmethod
    def remove(cls, ids_to_delete):
        return cls.objects.filter(pk__in=ids_to_delete).update(set__rejected_at=datetime.utcnow())


class BaseMongoengineStorage(BaseStorage):
    user = MongoengineUserMixin
    friendInvitation = MongoengineFriendInvitationMixin
    friendshipRequest = MongoengineFriendshipRequestMixin
    friends = MongoenginFriendsMixin