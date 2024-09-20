# Authentication

## Base auth logic

Authorization is based on the use of a jwt pair.

To get a pair of tokens, you need to log in using your firstname, lastname, email and password. If incorrect login and/or password values are passed, 401 HTTP status will be returned with `invalidCredentials` code in payload.

Access token is used to verify user requests. The access token has a short lifetime. If token is expired, 401 HTTP status will be returned with `expiredSignature` code in payload. Also can be returned 401 HTTP status with `invalidSignature`, if token can not be decode.

After the access token has expired, you need to send the request with refresh token to receive a new jwt pair.

## Refresh token validation

The issued refresh tokens are stored in the database. If a token is passed that is not in the database, 401 HTTP status will be returned with `invalidToken` code in payload. Also can be returned 401 HTTP status will be returned with `expiredSignature` code in payload. If that happens, you need to log in using your firstname, lastname, email and password again.
