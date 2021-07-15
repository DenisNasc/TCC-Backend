import bcrypt
from models.users import User


def authenticate(username, password):
    # None is the default value i.e if there is no username like the given.
    users = User.query.all()

    email_table = {u.email: u for u in users}

    user = email_table.get(username, None)

    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
        return user


def identity(payload):
    # extract the user id from that payload
    user = User.query.filter_by(id == payload["identity"]).first()

    return user
