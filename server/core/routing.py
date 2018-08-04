# In routing.py
from channels.routing import route

from server.apps.accounts.consumers import (
    users_ws_connect, users_ws_disconnect,
    users_ws_message, ws_add, ws_disconnect, ws_message
)

channel_routing = [
    route("users.websocket.connect", users_ws_connect),
    route("users.websocket.receive", users_ws_message),
    route("users.websocket.disconnect", users_ws_disconnect),

    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),


]
