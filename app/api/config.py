from datetime import timedelta, datetime
import requests


def black_list():
    from app.config import SELLER_OPERATOR_API_TOKEN, SELLER_BASE_API_URL

    try:
        black_list = requests.get(
            f"{SELLER_BASE_API_URL}/operator/security/blackwords",
            headers={"API-KEY": SELLER_OPERATOR_API_TOKEN},
        ).json()["black_words"]
        return black_list
    except ConnectionError:
        pass


TAG_CODE_PATTERN: str = r"[a-zA-Z0-9-!$%^&*()_+|~=`{}\[\]:\";'<>?,.\/\ \\]+"

MAX_TAG_CODE_LENGTH = 30

MAX_QUANTITY_OF_TAGS_PER_PRODUCT = 15

EXCEL_FILE_EXTENSIONS = ["XLSX", "XLS"]

ARCHIVE_FILE_EXTENSIONS = ["ZIP"]

PRODUCT_EXCEL_ERRORS_FILE = "product_errors"

PRODUCT_EXCEL_HEADERS = [
    "TITLE",
    "TYPE",
    "IN_STOCK",
    "PRICE",
    "OFFER_PRICE",
    "PROCESSING_MIN",
    "PROCESSING_MAX",
    "PERSONALIZATION",
    "PERSONALIZATION_TEXT",
    "PERSONALIZATION_LENGTH",
    "CATEGORY",
    "DESCRIPTION",
    "VIDEO_URL",
    "SECTION_NAME",
    "IMAGE1",
    "IMAGE2",
    "PREVIEW_IMAGE",
    "FILE",
    "TAGS",
    "OPTION1_NAME",
    "OPTION1_VALUES",
    "OPTION2_NAME",
    "OPTION2_VALUES",
]
DIGITAL_FILE_MAX_SIZE = 100_000_000

PRODUCT_EXCEL_DIGITAL_FILE_MAX_SIZE = 20_000_000

PRODUCT_EXCEL_IMAGE_MAX_SIZE = 2000000

PRODUCT_FILES_ARCHIVE_MAX_SIZE = 100000000

VIDEO_URL_PATTERN = r"^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"

ZIP_IGNORE = ["__MACOSX", ".DS_Store"]

EXCEL_ERRORS_FILE_EXPIRY = 2

TEMP_FILE_EXPIRY = 2

FIRST_REGIONS_TO_DESCRIBE_CODES = ["US", "EU", "NEU", "AUO"]

ETSY_REQUEST_LIMIT = 100
