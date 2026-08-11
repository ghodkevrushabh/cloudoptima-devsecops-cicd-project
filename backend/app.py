import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env'))

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from flask_sqlalchemy import SQLAlchemy

from generator import generate_iac
from git_sync import push_to_github

app = Flask(__name__)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

S3_STATE_BUCKET = os.getenv(
    "TF_STATE_BUCKET",
    "cloudoptima-tf-state-12345"
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# ---------------------------------------------------------
# Database Model
# ---------------------------------------------------------

class EnvironmentRequest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    app_name = db.Column(
        db.String(50),
        nullable=False
    )

    environment = db.Column(
        db.String(20),
        nullable=False
    )

    port = db.Column(
        db.Integer,
        nullable=False
    )

    instance_size = db.Column(
        db.String(20),
        nullable=False
    )

    repository_url = db.Column(
        db.String(500),
        nullable=True
    )

    branch = db.Column(
        db.String(100),
        nullable=False,
        default="main"
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.route("/")
def index():

    requests = (
        EnvironmentRequest.query
        .order_by(EnvironmentRequest.id.desc())
        .all()
    )

    return render_template(
        "index.html",
        requests=requests
    )


@app.route("/request", methods=["POST"])
def create_request():

    app_name = request.form["app_name"].strip()
    repository_url = request.form["repository_url"].strip()
    branch = request.form.get("branch", "main").strip()
    environment = request.form["environment"].strip()
    port = int(request.form["port"])
    instance_size = request.form["instance_size"].strip()

    # -----------------------------------------------------
    # Basic validation
    # -----------------------------------------------------

    if not app_name:
        return "Application name is required", 400

    if not repository_url.startswith(
        ("https://github.com/", "https://www.github.com/")
    ):
        return "Only GitHub repository URLs are supported", 400

    if not branch:
        return "Git branch is required", 400

    if port < 1 or port > 65535:
        return "Invalid application port", 400

    allowed_environments = {
        "dev",
        "staging",
        "prod"
    }

    if environment not in allowed_environments:
        return "Invalid environment", 400

    allowed_instance_types = {
        "t3.micro",
        "t3.small"
    }

    if instance_size not in allowed_instance_types:
        return "Invalid instance type", 400

    # -----------------------------------------------------
    # Save request
    # -----------------------------------------------------

    new_request = EnvironmentRequest(
        app_name=app_name,
        repository_url=repository_url,
        branch=branch,
        environment=environment,
        port=port,
        instance_size=instance_size,
        status="Pending"
    )

    db.session.add(new_request)
    db.session.commit()

    # -----------------------------------------------------
    # Generate IaC + Push to GitHub
    # -----------------------------------------------------

    try:

        generate_iac(
            app_name=app_name,
            environment=environment,
            port=port,
            instance_size=instance_size,
            s3_bucket_name=S3_STATE_BUCKET
        )

        # Push generated IaC to GitHub
        github_success = push_to_github(app_name)

        if not github_success:
            new_request.status = "GitPushFailed"
            db.session.commit()

            return "IaC generated, but GitHub push failed", 500

        new_request.status = "Generated"
        db.session.commit()

    except Exception as error:

        new_request.status = "GenerationFailed"
        db.session.commit()

        app.logger.exception(
            "IaC generation or GitHub push failed: %s",
            error
        )

        return "IaC generation failed", 500

    return redirect(url_for("index"))


# ---------------------------------------------------------
# Application startup
# ---------------------------------------------------------

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
