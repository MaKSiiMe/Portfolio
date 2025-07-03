from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Ajoute cette ligne juste après la création de app
