import os

import requests as basic_requests
import yaml
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow


class GoogleOAuth:
    def __init__(self, args):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        config = yaml.safe_load(open(config_path, "r"))
        if args.demo:
            self.config = config["GoogleOAuth"]["demo"]
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # localhostでhttpの場合のみ
        else:
            self.config = config["GoogleOAuth"]["production"]
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://accounts.google.com/o/oauth2/token",
                    "redirect_uris": self.config["redirect_uris"],
                }
            },
            scopes=self.config["scope"],
        )
        self.flow.redirect_uri = self.config["redirect_uri"]
        self.credentials = None

    def authorization_url(self) -> tuple:
        authorization_url, state = self.flow.authorization_url()
        return authorization_url, state

    def get_user_info(self) -> dict:
        if not self.credentials:
            return None
        endpoint = "https://www.googleapis.com/oauth2/v1/userinfo?"
        req_url = endpoint + f"access_token={self.credentials.token}"
        response = basic_requests.get(req_url)
        if response.status_code != 200:
            print("get_user_info Error: ", response.json())
            return None
        return response.json()

    def callback(
        self, request_url: str, request_state: str, session_state: str
    ) -> dict:
        if not session_state or session_state != request_state:
            raise Exception("CSRF攻撃を検知しました")
        self.flow.fetch_token(authorization_response=request_url)
        self.credentials = self.flow.credentials
        id_info = id_token.verify_oauth2_token(
            self.credentials.id_token, requests.Request(), self.client_id
        )
        user_info = id_info
        user_info.update(self.get_user_info())
        return user_info

    # def access_filter(self, user_info: dict) -> bool:
    #     if "hd" not in user_info or user_info["hd"] != "nkr-group.com":
    #         return False
    #     return True
