from datetime import datetime
import pytest
from lambda_file_server import lambda_function


def test_is_viewable_directory(mock_list_objects):
    assert lambda_function.is_viewable_directory("", mock_list_objects(""))


@pytest.fixture
def mock_list_objects():
    def _mock_list_objects(prefix):
        return "prefix"
        contents = [
            {"Key": key, "Size": 100, "LastModified": datetime(2020, 1, 2, 3, 4, 5)}
            for key in mock_s3_keys
        ]
        # common_prefixes =
        return {"Contents": contents}
    return _mock_list_objects


# Can use tuples in params to specify multiple values, which comma separated first value
# @pytest.mark.parametrize("key", ["1", "2"])
@pytest.fixture
def mock_s3_keys() -> list:
    return [
        "file" "hidden/file" "misc/file" "directoryA_extended" "directoryA/dir/file"
    ]


# @pytest.fixture(params=["hidden"])
# def test_is_viewable_directory(mock_list_objects):
#     assert mock_list_objects is not None

# {
#     "IsTruncated": True | False,
#     "Contents": [
#         {
#             "Key": "string",
#             "LastModified": datetime(2015, 1, 1),
#             "ETag": "string",
#             "ChecksumAlgorithm": [
#                 "CRC32" | "CRC32C" | "SHA1" | "SHA256",
#             ],
#             "Size": 123,
#             "StorageClass": "STANDARD"
#             | "REDUCED_REDUNDANCY"
#             | "GLACIER"
#             | "STANDARD_IA"
#             | "ONEZONE_IA"
#             | "INTELLIGENT_TIERING"
#             | "DEEP_ARCHIVE"
#             | "OUTPOSTS"
#             | "GLACIER_IR"
#             | "SNOW"
#             | "EXPRESS_ONEZONE",
#             "Owner": {"DisplayName": "string", "ID": "string"},
#             "RestoreStatus": {
#                 "IsRestoreInProgress": True | False,
#                 "RestoreExpiryDate": datetime(2015, 1, 1),
#             },
#         },
#     ],
#     "Name": "string",
#     "Prefix": "string",
#     "Delimiter": "string",
#     "MaxKeys": 123,
#     "CommonPrefixes": [
#         {"Prefix": "string"},
#     ],
#     "EncodingType": "url",
#     "KeyCount": 123,
#     "ContinuationToken": "string",
#     "NextContinuationToken": "string",
#     "StartAfter": "string",
#     "RequestCharged": "requester",
# }


def test_format_filesize_valid():
    assert lambda_function.format_filesize(1) == "1B"
    assert lambda_function.format_filesize(1024) == "1K"
    assert lambda_function.format_filesize(pow(1024, 2)) == "1M"


def test_format_filesize_invalid():
    with pytest.raises(ValueError):
        lambda_function.format_filesize(-1)
