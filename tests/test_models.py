from s3_util.models import User


def test_query_models(session):
    user = session.query(User).filter_by(login_name="root").first()
    assert user.id == 1
