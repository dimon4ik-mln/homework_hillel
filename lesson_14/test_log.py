#

import unittest
from lesson_14.homework_14 import log_event


class TestLogEvent(unittest.TestCase):

    def test_success_login_logged_as_info(self):
        with self.assertLogs("log_event", level="INFO") as log:
            log_event("admin", "success")

        self.assertIn(
            "INFO:log_event:Login event - Username: admin, Status: success",
            log.output
        )

    def test_expired_password_logged_as_warning(self):
        with self.assertLogs("log_event", level="WARNING") as log:
            log_event("user1", "expired")

        self.assertIn(
            "WARNING:log_event:Login event - Username: user1, Status: expired",
            log.output
        )

    def test_failed_login_logged_as_error(self):
        with self.assertLogs("log_event", level="ERROR") as log:
            log_event("user2", "failed")

        self.assertIn(
            "ERROR:log_event:Login event - Username: user2, Status: failed",
            log.output
        )


if __name__ == "__main__":
    unittest.main()
