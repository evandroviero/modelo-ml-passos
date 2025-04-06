from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config["SWAGGER"] = {
    "title": "My Flask API",
    "uiversion": 3
}

swagger = Swagger(app)

auth = HTTPBasicAuth()

users = {
    "user1": "password1",
    "user2": "password2"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    
def get_title(url):
    try:
        response = request.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip()
        return jsonify({"title": title})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scrape/title", methods=["GET"])
@auth.login_required
def scrape_title():
    """
    Extract the title of a web page provided by the URL
    ---
    security:
        - BasciAuth: []
    parameters:
        - name: url
          in: query
          type: string
          required: true
          description: URL of the web page
    responses:
        200:
            description: Web page title
    """
    url = request.args.get("url")
    if not url:
        return jsonify({"erro": "URL is required"}), 400
    return get_title(url)


def get_content(url):
    try:
        response = request.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        headers = []
        for header_tag in ["h1", "h2", "h3"]:
            for header in soup.find_all(header_tag):
                headers.append(header.get_text(strip=True))
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        return jsonify({"headers": headers, "paragraphs": paragraphs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/scrape/content", methods=["GET"])
@auth.login_required
def scrape_content():
    """
    Extract headers and paragraphs from web page provided by the URL
    ---
    security:
        - BasciAuth: []
    parameters:
        - name: url
          in: query
          type: string
          required: true
          description: URL of the web page
    responses:
        200:
            description: Web page title
    """
    url = request.args.get("url")
    if not url:
        return jsonify({"erro": "URL is required"}), 400
    return get_title(url)


if __name__ == "__main__":
    app.run(debug=True)
