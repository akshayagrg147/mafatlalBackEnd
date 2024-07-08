from decouple import config

database_config = {
    'NAME'      : config('DB_NAME'),       
    'USER'      : config('DB_USER'),       
    'PASSWORD'  : config('DB_PASSWORD'),
    'HOST'      : config('DB_HOST'),                
    'PORT'      : config('DB_PORT'),
}