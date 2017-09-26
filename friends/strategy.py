class BaseStrategy(object):
    def __init__(self, storage=None):
        self.storage = storage

    def authenticate_request(self, authorization):
        """
        Authenticate request user.
        :param authorization: request Authorization header value
        :return: authenticated user, None if no user found
        """
        raise NotImplementedError('Implement in subclass')

    def encryption_key(self):
        """
        return a string token used for serializing url
        http://pythonhosted.org/itsdangerous/
        :return:
        """
        raise NotImplementedError('Implement in subclass')


    def send_friendship_invitation_email(self, from_user, to_user_email, message):
        """Send email notification to non-existing user
        """
        raise NotImplementedError('Implement in subclass')

    def send_friendship_request_email(self, from_user, to_user, message, authentication_token):
        """
            Send email notification to existing user.
            authentication_token is a string encoded payload of
            {
              "from_user_id" : from_user_id,
              "to_user_id": to_user_id,
              "to_user_email": to_user_email (for non-existing user)
            }
            this token can be embedded in url and need to be passed back when accept/reject friend
        """
        raise NotImplementedError('Implement in subclass')