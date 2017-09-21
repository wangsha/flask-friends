class BaseStrategy(object):
    def __init__(self, storage=None):
        self.storage = storage

    def send_friendship_invitation_email(self, from_user, to_user_email, message):
        """Send email notification to non-existing user
        """
        raise NotImplementedError('Implement in subclass')

    def send_friendship_request_email(self, from_user, to_user, message):
        """Send email notification to existing user"""
        raise NotImplementedError('Implement in subclass')