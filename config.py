"""Top-level config module for backward compatibility and root-level scripts."""
from app.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, config_by_name

__all__ = ["Config", "DevelopmentConfig", "TestingConfig", "ProductionConfig", "config_by_name"]
