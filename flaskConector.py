# flaskConector.py
# Run with:  python flaskConector.py
from flask import Flask, request, jsonify, render_template
import golferSerch as gs  # your module; ok if it returns a dict or None

app = Flask(__name__)

@app.get("/")
def index():
    # Serves templates/index.html so the page and API share the same origin
    return render_template("index.html")

@app.get("/ping")
def ping():
    return "ok", 200

@app.post("/golferSerch")   # <-- matches your fetch URL exactly
def golferSerchByName():
    # Be forgiving with JSON parsing so the server never crashes
    data = request.get_json(silent=True) or {}

    firstName = (data.get("firstName") or "").strip().title()
    lastName  = (data.get("lastName")  or "").strip().title()

    if not firstName or not lastName:
        return jsonify({"message": "firstName and lastName are required"}), 400

    # ----- Pretend DB lookup (placeholder). Replace with your real call. -----
    # Try your real function:
    try:
        golfer = gs.lookUpGolfer(firstName, lastName)   # should return dict or None
    except Exception as e:
        # If your DB layer throws, show a clear error (so you don't get "Failed to fetch")
        return jsonify({"message": "Backend error", "detail": str(e)}), 500

    if not golfer:
        # Return 404 so the front end can show a friendly "not found"
        return jsonify({"message": "No matching golfer found."}), 404

    # Success: send the dictionary back as JSON
    return jsonify(golfer), 200

if __name__ == "__main__":
    import webbrowser
    from threading import Timer

    # This little function waits a moment for Flask to start, then opens the browser
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    # Start the timer to call open_browser() after 1 second
    Timer(1, open_browser).start()

    app.run(debug=True)



