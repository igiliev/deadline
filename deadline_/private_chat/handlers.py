import asyncio
import json
import logging
import re

import websockets
from django.contrib.auth import get_user_model
from django.db.models import Q

from accounts.models import User, Token
from private_chat.models import Dialog
from . import models, router
from django.contrib.sessions.models import Session

CONNECT_PATH_REGEX = r'^\/(?P<owner_id>\d{1,})\/(?P<owner_token>[a-z0-9]+)\/(?P<opponent_id>\d{1,})$'


def get_user_from_session(session_key):
    """
    Gets the user from current User model using the passed session_key
    :param session_key: django.contrib.sessions.models.Session - session_key
    :return: User instance or None if not found
    """
    session = Session.objects.get(session_key=session_key)
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    user = get_user_model().objects.filter(id=uid).first()  # get object or none
    return user


def get_or_create_dialog_with_users(user_owner, user_opponent):
    """
    Gets or creates the dialog between user_owner and user_opponent
    """
    if not Dialog.objects.filter(Q(owner=user_owner, opponent=user_opponent) | Q(opponent=user_owner, owner=user_opponent)).exists():
        return Dialog.objects.create(owner=user_owner, opponent=user_opponent)

    return Dialog.objects.filter(Q(owner=user_owner, opponent=user_opponent) | Q(opponent=user_owner, owner=user_opponent)).first()

logger = logging.getLogger('django-private-dialog')
ws_connections = {}


@asyncio.coroutine
def send_message(conn, payload):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    try:
        yield from conn.send(json.dumps(payload))
    except Exception as e:
        logger.debug('could not send', e)


@asyncio.coroutine
def fanout_message(connections, payload):
    """
    distributes payload (message) to all connected ws clients
    """
    for conn in connections:
        try:
            yield from conn.send(json.dumps(payload))
        except Exception as e:
            logger.debug('could not send', e)


@asyncio.coroutine
def gone_online(stream):
    """
    Distributes the users online status to everyone he has dialog with
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        if session_id:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                logger.debug('User '+user_owner.username+' gone online')
                # find all connections including user_owner as opponent,
                # send them a message that the user has gone online
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                online_opponents_sockets = [ws_connections[i] for i in online_opponents]
                yield from fanout_message(online_opponents_sockets,
                                          {'type': 'gone-online', 'usernames': [user_owner.username]})
            else:
                pass  # invalid session id
        else:
            pass  # no session id


@asyncio.coroutine
def check_online(stream):
    """
    Used to check user's online opponents and show their online/offline status on page on init
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        opponent_username = packet.get('username')
        if session_id and opponent_username:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                # Find all connections including user_owner as opponent
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                logger.debug('User '+user_owner.username+' has '+str(len(online_opponents))+' opponents online')
                # Send user online statuses of his opponents
                socket = ws_connections.get((user_owner.username, opponent_username))
                if socket:
                    online_opponents_usernames = [i[0] for i in online_opponents]
                    yield from send_message(socket,
                                              {'type': 'gone-online', 'usernames': online_opponents_usernames})
                else:
                    pass  # socket for the pair user_owner.username, opponent_username not found
                    # this can be in case the user has already gone offline
            else:
                pass  # invalid session id
        else:
            pass  # no session id or opponent username


@asyncio.coroutine
def gone_offline(stream):
    """
    Distributes the users online status to everyone he has dialog with
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        if session_id:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                logger.debug('User '+user_owner.username+' gone offline')
                # find all connections including user_owner as opponent,
                #  send them a message that the user has gone offline
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                online_opponents_sockets = [ws_connections[i] for i in online_opponents]
                yield from fanout_message(online_opponents_sockets,
                                          {'type': 'gone-offline', 'username': user_owner.username})
            else:
                pass  # invalid session id
        else:
            pass  # no session id


@asyncio.coroutine
def new_messages_handler(stream):
    """
    Saves a new chat message to db and distributes msg to connected users

    Needs to be sent the following JSON
    {
        "type": "new-message",
        "message": "YOUR_MESSAGE_HERE",
        "user_id": YOUR_USER_ID_HERE,
        "opponent_id": HIS_ID_HERE
    }
    """
    # TODO: handle no user found exception
    while True:
        packet = yield from stream.get()
        # TODO: Validate JSON
        # TODO: Think up of a way to validate the user, most likely his Token?
        # TODO: Absolutely needs validation
        # TODO: Maybeu nique session key per Dialog?
        # print(vars(packet))
        print('Distributing message')
        message = packet.get('message')
        user_owner = User.objects.get(id=packet.get('user_id'))
        user_opponent = User.objects.get(id=packet.get('opponent_id'))

        print(f'User opponent is {user_opponent}')
        dialog: Dialog = get_or_create_dialog_with_users(user_owner, user_opponent)
        print(f'Dialog is {dialog}')

        # Save the message
        msg = models.Message.objects.create(
            dialog=dialog,
            sender=user_owner,
            text=packet['message']
        )
        packet['created'] = msg.get_formatted_create_datetime()
        packet['sender_name'] = msg.sender.username

        # Send the message to both parties
        connections = []
        if (user_owner.id, user_opponent.id) in ws_connections:
            connections.append(ws_connections[(user_owner.id, user_opponent.id)])
        # Find socket of the opponent
        if (user_opponent.id, user_owner.id) in ws_connections:
            connections.append(ws_connections[(user_opponent.id, user_owner.id)])

        yield from fanout_message(connections, packet)

# @asyncio.coroutine
# def users_changed_handler(stream):
#     """
#     Sends connected client list of currently active users in the chatroom
#     """
#     while True:
#         yield from stream.get()
#
#         # Get list list of current active users
#         users = [
#             {'username': username, 'uuid': uuid_str}
#             for username, uuid_str in ws_connections.values()
#         ]
#
#         # Make packet with list of new users (sorted by username)
#         packet = {
#             'type': 'users-changed',
#             'value': sorted(users, key=lambda i: i['username'])
#         }
#         logger.debug(packet)
#         yield from fanout_message(ws_connections.keys(), packet)

#
# @asyncio.coroutine
# def is_typing_handler(stream):
#     """
#     Show message to opponent if user is typing message
#     """
#     while True:
#         packet = yield from stream.get()
#         session_id = packet.get('session_key')
#         user_opponent = packet.get('username')
#         typing = packet.get('typing')
#         if session_id and user_opponent and typing is not None:
#             user_owner = get_user_from_session(session_id)
#             if user_owner:
#                 opponent_socket = ws_connections.get((user_opponent, user_owner.username))
#                 if typing and opponent_socket:
#                     yield from target_message(opponent_socket,
#                                               {'type': 'opponent-typing', 'username': user_opponent})
#             else:
#                 pass  # invalid session id
#         else:
#             pass  # no session id or user_opponent or typing


@asyncio.coroutine
def main_handler(websocket, path):
    """
    An Asyncio Task is created for every new websocket client connection
    that is established. This coroutine listens to messages from the connected
    client and routes the message to the proper queue.

    This coroutine can be thought of as a producer.

    Expected path for initial connection is
    /user_id/user_token/user_to_speak_to_id
    """
    # Get users name from the path
    owner_id, owner_token, opponent_id = extract_path(path)
    try:
        owner, opponent = fetch_and_validate_participants(owner_id, owner_token, opponent_id)
    except (ChatPairingError, UserTokenMatchError, User.DoesNotExist, Token.DoesNotExist) as e:
        print(str(e))
        return

    # owner = owner.username
    # Persist users connection, associate user w/a unique ID
    ws_connections[(owner.id, opponent.id)] = websocket
    # TODO: Create Dialog here and give the session_id
    yield from send_message(websocket, {'tank': 'YOU ARE CONNECTED :)'})
    # While the websocket is open, listen for incoming messages/events
    # if unable to listening for messages/events, then disconnect the client
    try:
        while websocket.open:
            data = yield from websocket.recv()
            if not data:
                continue

            logger.debug(data)

            try:
                print(f'Data is {data}')
                yield from router.MessageRouter(data)()
            except Exception as e:
                logger.error('could not route msg', e)

    except websockets.exceptions.InvalidState:  # User disconnected
        pass
    finally:
        del ws_connections[(owner.id, opponent.id)]


class Error(Exception):
    pass


class RegexMatchError(Error):
    """ Used when we cannot match with regex """
    pass


class ChatPairingError(Error):
    pass


class UserTokenMatchError(Error):
    pass


def extract_path(path):
    """
    Sample path: /user_id/user_token/user_to_speak_to_id
    """
    match_obj = re.match(CONNECT_PATH_REGEX, path)
    if match_obj is None:
        raise RegexMatchError(f'Path {path} does not match the expected regex!')
    regex_groups = match_obj.groupdict()
    owner_id = int(regex_groups['owner_id'])
    owner_token = regex_groups['owner_token']
    opponent_id = int(regex_groups['opponent_id'])

    return owner_id, owner_token, opponent_id


def fetch_and_validate_participants(owner_id: int, owner_token: str, opponent_id: int) -> (User, User):
    """
    Fetches the User objects and validates them
    """
    if owner_id == opponent_id:
        raise ChatPairingError('Cannot match a user to himself!')
    token = Token.objects.get(key=owner_token)
    owner = User.objects.get(id=owner_id)

    # Validate the token is correct
    if owner.auth_token.key != owner_token or token.user_id != owner_id:
        raise UserTokenMatchError(f'User with ID {owner_id} does not have a token {owner_token}')

    opponent = User.objects.get(id=opponent_id)

    return owner, opponent
