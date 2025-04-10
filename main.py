from flask import Flask
from config import configure_all
import scheduler_startup


app= Flask(__name__)


configure_all(app)
app.run(debug=False, host='0.0.0.0', port=5000)


