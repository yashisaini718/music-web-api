from app import create_app
from app.extensions import db
from app.utils.token_cleanup import cleanup_expired_tokens

app = create_app()

with app.app_context():
    try:
        cleanup_expired_tokens()
        app.logger.info(f"Deleted expired tokens")
    except Exception as e:
        app.logger.warning(f"Token cleanup failed: {e}")