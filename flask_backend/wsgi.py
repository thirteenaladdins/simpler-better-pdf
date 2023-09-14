from routes.server import app
import os
 
if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 3000))
    # app.run(threaded=True, host="0.0.0.0", port=port)
    app.run(threaded=True, host='0.0.0.0', port=591)

