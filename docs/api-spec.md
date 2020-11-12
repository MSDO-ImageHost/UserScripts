# API Specification

## Create User Script

Endpoint: `userscripts/createUserScript`

Request
```json
{
    "filename": "<file>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "user_script": "<script id>",
    "http_status": "<integer>",
    "created_at": "<ISO8601 timestamp>"
}
```

## Request User Script Status

Endpoint: `userscripts/requestUserScriptStatus`

Request
```json
{
    "user_script": "<script id>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "script_running_status": "<boolean>"
}
```

## Update User Script

Endpoint: `userscripts/updateUserScript`

Request
```json
{
    "user_script": "<script id>",
    "filename": "<file>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "http_status": "<integer>",
    "updated_at": "<ISO8601 timestamp>"
}
```

## Delete User Script

Endpoint: `userscripts/deleteUserScript`

Request
```json
{
    "user_script": "<script id>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "http_status": "<integer>",
    "deleted_at": "<ISO8601 timestamp>"
}
```
