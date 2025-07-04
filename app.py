from flask import Flask, request, jsonify
from email_utils import send_email

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    recipient = data.get("recipient")
    subject = data.get("subject", "Default Subject")
    name = data.get("name", "User")

    if not recipient:
        return jsonify({"error": "Recipient email is required"}), 400

    context = {
        "name": name,
        "text": f"Hello {name}, welcome to our service!"
    }

    result = send_email(recipient, subject, "email_template.html", context)
    return jsonify(result), 200 if result['status'] == "success" else 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

