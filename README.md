# GoogleOAuth

## settings

1. add .env file

   ```sh
   CLIENT_ID=your_client_id
   CLIENT_SECRET=your_client_secret
   ```

2. edit config.yaml

   - edit target

     - `GoogleOAuth.demo.redirect_uris`: redirect_uris which is set in GCP console
     - `GoogleOAuth.demo.redirect_uri`: redirect_uri which is using in demo program
     - `GoogleOAuth.production.redirect_uris`: redirect_uris which is set in GCP console
     - `GoogleOAuth.production.redirect_uri`: redirect_uri which is using in production program

   - sample:

   ```yaml
    GoogleOAuth:
        demo:
            redirect_uris: ["http://127.0.0.1:5000/oauth2callback"]
            redirect_uri: "http://127.0.0.1:5000/oauth2callback"
            scope:
            [
                "openid",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ]
        production:
            redirect_uris: ["https://oauthtest-eidnwbgjma-an.a.run.app/oauth2callback"]
            redirect_uri: "https://oauthtest-eidnwbgjma-an.a.run.app/oauth2callback"
            scope:
            [
                "openid",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ]
   ```
