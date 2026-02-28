from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

@app.route("/like")
def like():
    uid = request.args.get("uid")
    region = request.args.get("region")

    if not uid or not region:
        return jsonify({"error": "Missing uid or region"}), 400

    # Vercel API call
    url = f"https://info-canze1.vercel.app/player-info?uid={uid}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch player info"}), 500
        data = response.json()
    except Exception as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

    # Region check
    actual_region = data.get("basicInfo", {}).get("region", "").upper()
    if region.upper() != actual_region:
        return jsonify({"error": "Invalid pattern"}), 400

    # Extract required info
    nickname = data.get("basicInfo", {}).get("nickname", "Unknown")
    liked_before = data.get("basicInfo", {}).get("liked", 0)

    # Simulate like increment (mostly +20, sometimes +18 or +19)
    increment = random.choices([18,19,20], weights=[0.01,0.01,0.98])[0]
    liked_after = liked_before + increment

    result = {
        "name": nickname,
        "uid": uid,
        "region": actual_region,
        "like": {
            "before": liked_before,
            "after": liked_after,
            "Give": increment
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)