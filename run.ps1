# Set up flask environemt
./venv/Scripts/activate
$env:FLASK_ENV = "development"

# Set Search engine ID:
$env:GCS_ENGINE_ID = "your_id"

# Set Custom Search JSON API Key : 
$env:GCS_API_KEY = "your_key"

# Run
flask run