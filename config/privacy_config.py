from pydantic_settings import BaseSettings, SettingsConfigDict


class PrivacyConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    pii_detection_enabled: bool = True
    pii_token_expiry_seconds: int = 3600
    pii_token_prefix: str = "[PII_"
    pii_token_suffix: str = "]"

    # Indian PII (DPDP compliance)
    detect_aadhaar: bool = True
    detect_pan: bool = True
    detect_passport: bool = True
    detect_driving_license: bool = True
    detect_upi_id: bool = True

    # Standard PII
    detect_email: bool = True
    detect_phone: bool = True
    detect_name: bool = True
    detect_address: bool = True
    detect_dob: bool = True

    audit_logging_enabled: bool = True
    log_rehydration_events: bool = True


privacy_config = PrivacyConfig()