from pydantic import BaseModel

# x-release-please-start-version
API_VERSION = '0.0.1'
# x-release-please-end


class ApiVersionOutDTO(BaseModel):
    version: str


def get_api_version() -> ApiVersionOutDTO:
    return ApiVersionOutDTO(version=API_VERSION)
