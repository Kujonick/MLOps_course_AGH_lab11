from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field, field_validator


class Settings(BaseSettings):
    bucket: str = Field(..., alias="BUCKET")
    prefix: str = Field(..., alias="PREFIX")
    resource_dir: Path = Field(..., alias="RESOURCE_DIR")
    embedding_dim:int = 384

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @field_validator("prefix")
    @classmethod
    def normalize_prefix(cls, v: str) -> str:
        return v.strip("/").rstrip("/") + "/"

    @field_validator("resource_dir")
    @classmethod
    def validate_local_dir(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def classifier_joblib_path(self) -> Path:
        path = self.resource_dir / "classifier.joblib"
        return path

    @property
    def sentence_transformer_dir(self) -> Path:
        path = self.resource_dir / "sentence_transformer.model"
        return path
    
    @property
    def onnx_classifier_path(self) -> Path:
        path = self.resource_dir / "classifier.onnx"
        return path
    
    @property
    def onnx_embedding_model_path(self) -> Path:
        path = self.resource_dir / 'embedding_model.onnx'
        return path
    
    @property
    def onnx_tokenizer_dir(self) -> Path:
        path = self.resource_dir / 'onnx_tokenizer'
        path.mkdir(parents=True, exist_ok=True)
        return path
    