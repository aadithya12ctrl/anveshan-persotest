from pydantic_settings import BaseSettings, SettingsConfigDict


class MonitoringThresholds(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Daily limits in minutes
    default_daily_threshold: int = 120
    social_media_threshold: int = 60
    entertainment_threshold: int = 90
    gaming_threshold: int = 60
    news_threshold: int = 45
    productivity_threshold: int = 480

    # Breach severity (multiplier over baseline)
    minor_breach_multiplier: float = 1.25
    moderate_breach_multiplier: float = 1.5
    severe_breach_multiplier: float = 2.0

    # Intervention limits
    intervention_cooldown_minutes: int = 30
    max_interventions_per_day: int = 5

    # Baseline calculation
    baseline_window_days: int = 14
    baseline_min_data_days: int = 3


monitoring_thresholds = MonitoringThresholds()