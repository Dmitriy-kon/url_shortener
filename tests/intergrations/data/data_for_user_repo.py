from contextlib import nullcontext as not_raise

import pytest
from sqlalchemy.exc import IntegrityError

data_for_create_user = [
    ("test_user21", "testpassword20", not_raise()),
    ("test_user21", "testpassword21", pytest.raises(IntegrityError)),
    ("test_user22", None, pytest.raises(IntegrityError)),
    (None, "testpassword22", pytest.raises(IntegrityError)),
]

data_for_change_user = [
    ("test_user31", "testpassword31"),
    ("test_user32", "testpassword32"),
]

data_for_delete_user = [
    ("test_user41", "testpassword41"),
    ("test_user42", "testpassword42"),
]

data_for_get_user_by_username = [
    ("test_user51", "testpassword51"),
    ("test_user52", "testpassword52"),
]

data_for_get_user_by_id = [
    ("test_user61", "testpassword61"),
    ("test_user62", "testpassword62"),
]
