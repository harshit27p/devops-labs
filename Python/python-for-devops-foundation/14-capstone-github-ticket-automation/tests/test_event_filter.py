from github_events import should_create_ticket

def test_expected_comment_is_accepted():
    payload = {
        "action": "created",
        "repository": {"full_name": "owner/repo"},
        "issue": {"number": 12},
        "comment": {"body": "/jira"},
    }
    assert should_create_ticket("issue_comment", payload, "owner/repo")

def test_other_comment_is_ignored():
    payload = {
        "action": "created",
        "repository": {"full_name": "owner/repo"},
        "issue": {"number": 12},
        "comment": {"body": "please investigate"},
    }
    assert not should_create_ticket("issue_comment", payload, "owner/repo")
