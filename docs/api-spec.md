# API Specification

## Create User Script

Request
```json
{
    "program": "[file]",
    "main_file": "<filename>",
    "language": "<code_language>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "user_script": "<script id>",
    "http_status": "<integer>",
}
```

## Request User Script Status

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

Request
```json
{
    "user_script": "<script id>",
    "updated_files": "[file]",
    "updated_main_file": "<filename>",
    "updated_language": "<code_language>",
    "authentication_token": "<jwt>"
}
```

Response
```json
{
    "http_status": "<integer>",
}
```

## Delete User Script

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
    "http_status": "<integer>"
}
```


## Run User Script

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
    "http_status": "<integer>"
}
```
