from decouple import config

database_config = {
    'NAME'      : config('DB_NAME'),       
    'USER'      : config('DB_USER'),       
    'PASSWORD'  : config('DB_PASSWORD'),
    'HOST'      : config('DB_HOST'),                
    'PORT'      : config('DB_PORT'),
}

S3_config = {
    "AWS_ACCESS_KEY_ID"     : config('AWS_ACCESS_KEY_ID'),
    "AWS_SECRET_ACCESS_KEY" : config('AWS_SECRET_ACCESS_KEY'),
    "REGION_NAME"           : config('REGION_NAME'),
}