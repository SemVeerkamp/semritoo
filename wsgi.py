from website import create_app
import os

port = int(os.environ.get('PORT', 33507))

app = create_app()

app.run(debug=True, port=port)
