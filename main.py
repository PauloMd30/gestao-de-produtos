from flask import Flask
from config import configure_all
from scheduler_startup import start_scheduler


app= Flask(__name__)


configure_all(app)
start_scheduler()
#app.run(debug=True)
app.run(debug=False, host='0.0.0.0', port=5000)


