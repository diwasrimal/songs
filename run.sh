#!/bin/bash

# Setup environment
. venv/bin/activate
export FLASK_ENV=development

# Set enviroment variables
export GCS_API_KEY=your_key
export GCS_ENGINE_ID=your_id

# Run the server
flask run