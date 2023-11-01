class BaseMessage:
    """
    Base message class used for composing emails to be sent
    to users
    """

    MESSAGE = None
    SUBJECT = None

    def __init__(self, context) -> None:
        self.context = context

    def to_message(self):
        return self.MESSAGE.format(**self.context)


class EmailVerification(BaseMessage):
    """
    Message for OTP for verifying a user
    """

    SUBJECT = "OTP for signup :fire"
    MESSAGE = """
    Hi there, click on the link to complete your signup:
    {link}.
    It will expire in {duration} minutes.
    """


# class ForgotPasswordMessage(BaseMessage):
#     """
#     Message for OTP for forgot password
#     """
#     SUBJECT = "OTP for change password :water"
#     MESSAGE = """
#     Hi there, you requested a change in password. Use this OTP
#     to complete the password change process:
#     {otp}
#     It will expire in {duration} minutes.
#     """


# class InviteUser(BaseMessage):
#     """
#     Message for inviting a user to a client
#     """

#     SUBJECT = "You have been invited to a client"
#     MESSAGE = """
#     Hi there, {full_name} has invited you to the role of {role}
#     in their client, {client_name}.

#     Click on this link to accept their invite: {link}.
#     """
