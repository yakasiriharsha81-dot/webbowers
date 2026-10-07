"""Application launcher and CLI commands for Polar Science Hub."""
import os
import click
from app import create_app
from app.extensions import db
from seed.seed_demo import seed_database

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.cli.command("seed-demo")
def seed_demo_command():
    """Seeds the database with comprehensive, explicitly marked DEMO DATA."""
    with app.app_context():
        seed_database()
        click.echo("✓ Demo database initialized and loaded with synthetic demo records.")


@app.cli.command("init-db")
def init_db_command():
    """Initializes tables from SQLAlchemy models."""
    with app.app_context():
        db.create_all()
        click.echo("✓ Database tables created.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
