class UserMixin(object):
    @classmethod
    def get_id(cls, user):
        """Return the ID for given user"""
        return getattr(user, cls.id_field(), None)

    @classmethod
    def get_email(cls, user):
        """Return the email for given user"""
        return getattr(user, cls.email_field(), None)

    @classmethod
    def username_field(cls):
        return getattr(cls.user_model(), "USERNAME_FIELD", "username")

    @classmethod
    def id_field(cls):
        return getattr(cls.user_model(), "ID_FIELD", "id")

    @classmethod
    def email_field(cls):
        return getattr(cls.user_model(), "EMAIL_FIELD", "email")

    @classmethod
    def user_model(cls):
        """Return the user model"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def user_exisits(cls, email):
        """
        Return True/False if a User instance exists with given email address.
        :param email: String
        :return: Boolean
        """
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_user_by_email(cls, email):
        """Return user instance for given email address"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_user_by_id(cls, id):
        """Return user instance for given id"""
        raise NotImplementedError("Implement in subclass")


class FriendInvitationMixin(object):
    """
    Friendship invitation to non-exisiting users.
    """

    from_user = ""
    to_user_email = ""
    message = ""

    @classmethod
    def create(cls, from_user, to_user_email, message):
        """Create a friendship invitation"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_invitations_by_email(cls, to_user_email):
        """Return friendship invitations with given to_user_email   """
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_invitations_by_from_user(cls, from_user):
        """Return friendship invitations with given from_user   """
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def remove(cls, ids_to_delete):
        """Remove objects with given ids"""
        raise NotImplementedError("Implement in subclass")


class FriendshipRequestMixin(object):
    from_user = ""
    to_user = ""
    message = ""
    rejected_at = ""

    @classmethod
    def create(cls, from_user, to_user, message=None):
        """Create a friendship request"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_request(cls, from_user, to_user):
        """Return a non-rejected friendship request"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_request_by_from_user(cls, from_user):
        """Return non-rejected friendship requests initiated by given from_user"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_request_by_to_user(cls, to_user):
        """Return non-rejected friendship requests made to given to_user"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_rejected_request_by_from_user(cls, from_user):
        """Return rejected friendship requests initiated by given from_user"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_rejected_request_by_to_user(cls, to_user):
        """Return rejected friendship requests made to given to_user"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def remove(cls, ids_to_delete):
        """Remove objects with given ids"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def reject(cls, ids_to_reject):
        """Reject objects with given ids"""
        raise NotImplementedError("Implement in subclass")


class FriendsMixin(object):
    user1 = ""
    user2 = ""

    @classmethod
    def create(cls, user1, user2):
        """Create a friends relaship"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def remove_friend(cls, user1, user2):
        """Create a friends relaship"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def get_friends(cls, user):
        """Return friends with given user"""
        raise NotImplementedError("Implement in subclass")

    @classmethod
    def remove(cls, ids_to_delete):
        """Remove objects with given ids"""
        raise NotImplementedError("Implement in subclass")


class BaseStorage(object):
    user = UserMixin
    friendInvitation = FriendInvitationMixin
    friendshipRequest = FriendshipRequestMixin
    friends = FriendsMixin
