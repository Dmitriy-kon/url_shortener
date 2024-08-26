from contextlib import nullcontext as not_raise

import pytest
from sqlalchemy.exc import IntegrityError

data_for_insert_test = [
    ("test_user1", "testpassword", "https://example.com", "asdasSSH@", not_raise()),
    (
        "test_user2",
        "testpassword2",
        "https://another-example.com",
        "ZH^YHSAGHD*@HS",
        not_raise(),
    ),
    (
        "test_user3",
        "testpassword3",
        "https://yet-another-example.com",
        "short1",
        not_raise(),
    ),
    (
        "test_user4",
        "testpassword4",
        "https://yet-another-example.com",
        "short1",
        pytest.raises(IntegrityError),
    ),
    (
        "test_user5",
        "testpassword5",
        None,
        "asdasdzxc645",
        pytest.raises(IntegrityError),
    ),
    (
        "test_user6",
        "testpassword6",
        "https://yet-another-example.com",
        None,
        pytest.raises(IntegrityError),
    ),
]


data_for_change_test = [
    ("test_user7", "testpassword7", "https://example2.com", "asdasSSHzxczx@"),
    ("test_user8", "testpassword8", "https://examplezxczx.com", "asdasSSHzx5sczx@"),
]

data_for_click_url_test = [
    ("test_user9", "testpassword9", "https://example5.com", "s65asdasSSHzxczx@"),
    (
        "test_user10",
        "testpassword10",
        "https://exampl6ezxczx.com",
        "s21asdasSSHzx5sczx@",
    ),
]

data_for_delete_test = [
    ("test_user11", "testpassword11", "https://example7.com", "xzczxcaq12312@"),
    ("test_user12", "testpassword12", "https://example8.com", "hdfg*@Szx@"),
]

data_for_all_user_urls_test = [
    (
        "test_user13",
        "testpassword13",
        (
            ("https://example9.com", "asdasSSHzxczxcsF@"),
            ("https://example10.com", "JS&JXK&SSHzx5sczxcsF@"),
        ),
        20,
        0,
    ),
    (
        "test_user14",
        "testpassword14",
        (
            ("https://example11.com", "asdasSsdfsdSHzxczxcsF@"),
            ("https://example112.com", "JS&JXK&SSHsdfv12$zx5sczxcsF@"),
        ),
        20,
        1,
    ),
]
data_for_get_url_by_short_url = [
    (
        "test_user15",
        "testpassword15",
        "https://example12.com",
        "asdzxczxasSSHzxczxcsF@",
    ),
    (
        "test_user16",
        "testpassword16",
        "https://example13.com",
        "asdzxczxasSSHzxczxczxcsF@",
    ),
]

data_for_get_url_by_userid_and_url = [
    ("test_user17", "testpassword17", "https://example14.com", "asdzxczxaz123SczxcsF@"),
    (
        "test_user18",
        "testpassword18",
        "https://example15.com",
        "asdzxczxaKN&s1SczxcsF@",
    ),
]

data_for_get_url_by_url_id = [
    ("test_user19", "testpassword19", "https://example16.com", "asdzxczxasSSJH&SxcsF@"),
    (
        "test_user20",
        "testpassword20",
        "https://example17.com",
        "asdzP)xasS<M&SHzxczxczxcsF@",
    ),
]
