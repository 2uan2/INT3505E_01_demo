from flask import Flask, request
import requests
import base64
import uuid

app = Flask(__name__)

users = []
sessions = {}

@app.route("/register", methods=['POST'])
def register():
    try: 
        username = request.json['username']
        password = request.json['password']
        if username not in [user['username'] for user in users]:
            cookie = uuid.uuid4()
            new_user = {
                'username': username,
                'password': password,
            }
            sessions[str(cookie)] = new_user
            users.append(new_user)
            return {'cookie': cookie}, 201
        else: 
            return {'message': 'username unavailable'}, 409
    except Exception as e:
        print(e)
        return {'message': 'something went wrong'}, 500

@app.route("/login", methods=['POST'])
def login():
    try: 
        username = request.json['username']
        password = request.json['password']
        for user in users:
            if username == user['username'] and password == user['password']:
                cookie = uuid.uuid4()
                sessions[str(cookie)] = user
                return {'cookie': cookie}, 200

        return {'message': 'wrong credential'}, 409
    except:
        return {'message': 'something went wrong'}, 500

@app.route("/logout", methods=['POST'])
def logout():
    try:
        cookie = request.cookies.get('session_id')
        del sessions[str(cookie)]
    except:
        return {'message': 'something went wrong'}, 500

@app.route("/private")
def private_route():
    user = authenticate_request(request)

    if not user:
        return {'message': 'wrong credentials'}, 401
    return 'secret content\n'

def authenticate_request(request):
    print(request.headers.get('Authorization'))
    auth = request.headers.get('Authorization')
    if auth:
        return
    
        if auth.startswith("Basic"):
            base64_string = auth.split("Basic")[1].strip()
            decoded_data = base64.b64decode(base64_string)
            [username, password] = decoded_data.decode('utf-8').split(':')
            for user in users:
                if username == user['username'] and password == user['password']:
                    return user

        # if auth.startswith("Bearer"):
        #     cookie = auth.split("Bearer")[1].strip()
        #     for user in users:
        #         print("user's cookie:", user['cookie'])
        #         print("bearer:", cookie)
        #         if user['cookie'] == cookie:
        #             return user
    cookie = request.cookies.get('session_id')
    if cookie:
        print(cookie)
        return sessions[cookie]
    
@app.route("/c")
def get_cookies():
    return sessions

# def authenticated(rule: str, **options: t.Any) -> t.Callable[[T_route], T_route]: """Decorate a view function to register it with the given URL
#     rule and options. Calls :meth:`add_url_rule`, which has more
#     details about the implementation.
#
#     .. code-block:: python
#
#         @app.route("/")
#         def index():
#             return "Hello, World!"
#
#     See :ref:`url-route-registrations`.
#
#     The endpoint name for the route defaults to the name of the view
#     function if the ``endpoint`` parameter isn't passed.
#
#     The ``methods`` parameter defaults to ``["GET"]``. ``HEAD`` and
#     ``OPTIONS`` are added automatically.
#
#     :param rule: The URL rule string.
#     :param options: Extra options passed to the
#         :class:`~werkzeug.routing.Rule` object.
#     """
#
#     def decorator(f: T_route) -> T_route:
#         endpoint = options.pop("endpoint", None)
#         self.add_url_rule(rule, endpoint, f, **options)
#         return f
#
#     return decorator
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
