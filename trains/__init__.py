from flask import Flask

app = Flask('trains')

try:
    import trains.trainsApp
except Exception as e:
    print (str(e))