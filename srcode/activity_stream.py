import datetime
from config import Config
import stream 
stream_api_key = Config.stream_api_key
stream_secret_key = Config.stream_secret_key

#!CREATE NEW STREAM CLIENT
client = stream.connect(api_key=stream_api_key, api_secret=stream_secret_key)

#!CREATE A NEW STREAM CLIENT SPECIFIYING DATACENTER LOCATION
client = stream.connect(stream_api_key, stream_secret_key, location='us-east')

