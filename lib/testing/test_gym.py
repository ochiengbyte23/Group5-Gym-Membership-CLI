import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json
import main
from unittest.mock import patch, MagicMock
from argparse import Namespace

# ---------------------------------------------------------------------------
# Minimal stubs for the lib.* classes so tests run without the full project
# ---------------------------------------------------------------------------

class _User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.membership_plan = "none"

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "email": self.email, "membership_plan": self.membership_plan}

    def __str__(self):
        return f"{self.name} ({self.email})"


class _Trainer:
    def __init__(self, id, name, experience):
        self.id = id
        self.name = name
        self.experience = experience
        self.trainees_id = []

    def to_dict(self):
        return {"id": self.id, "name": self.name,
                "experience": self.experience, "trainees_id": self.trainees_id}

    def __str__(self):
        return f"{self.name} ({self.experience} yrs)"


class _Admin:
    def __init__(self, admin_id, trainer_id, user_id, schedule, status):
        self.id = admin_id
        self.trainer_id = trainer_id
        self.user_id = user_id
        self.schedule = schedule
        self.status = status

    def to_dict(self):
        return {"id": self.id, "trainer_id": self.trainer_id,
                "user_id": self.user_id, "schedule": self.schedule,
                "status": self.status}


class _Membership:
    pass


# Patch lib imports before importing main
sys.modules.setdefault("lib", MagicMock())
sys.modules["lib.User"]       = MagicMock(User=_User)
sys.modules["lib.Trainer"]    = MagicMock(Trainer=_Trainer)
sys.modules["lib.Admin"]      = MagicMock(Admin=_Admin)
sys.modules["lib.Membership"] = MagicMock(Membership=_Membership)

import main  # noqa: E402  (imported after stubs)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_args(**kwargs):
    """Build a simple Namespace the same way argparse would."""
    return Namespace(**kwargs)


# ---------------------------------------------------------------------------
# Tests for add_user
# ---------------------------------------------------------------------------

class TestAddUser:
    def test_add_user_saves_to_file(self, tmp_path, monkeypatch, capsys):
        users_file = tmp_path / "users.json"
        users_file.write_text("[]")

        monkeypatch.setattr(main, "USERS_FILE", str(users_file))
        monkeypatch.setattr(main, "load", lambda _: json.loads(users_file.read_text()))
        monkeypatch.setattr(main, "save", lambda path, data: users_file.write_text(json.dumps(data)))

        main.add_user(make_args(name="Alice", email="alice@example.com"))

        saved = json.loads(users_file.read_text())
        assert len(saved) == 1
        assert saved[0]["name"] == "Alice"
        assert saved[0]["email"] == "alice@example.com"

    def test_add_user_prints_confirmation(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.add_user(make_args(name="Bob", email="bob@example.com"))

        assert "Bob" in capsys.readouterr().out

    def test_add_user_id_increments(self, monkeypatch):
        existing = [{"id": 1, "name": "X", "email": "x@x.com", "membership_plan": "none"}]
        saved = []
        monkeypatch.setattr(main, "load", lambda _: list(existing))
        monkeypatch.setattr(main, "save", lambda _, data: saved.extend(data))

        main.add_user(make_args(name="New", email="new@example.com"))

        assert saved[-1]["id"] == 2


# ---------------------------------------------------------------------------
# Tests for list_users
# ---------------------------------------------------------------------------

class TestListUsers:
    def test_list_users_empty(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        main.list_users(make_args())
        assert "No users found" in capsys.readouterr().out

    def test_list_users_shows_all(self, monkeypatch, capsys):
        users = [
            {"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "gold"},
            {"id": 2, "name": "Bob",   "email": "b@b.com", "membership_plan": "none"},
        ]
        monkeypatch.setattr(main, "load", lambda _: users)
        main.list_users(make_args())
        out = capsys.readouterr().out
        assert "Alice" in out
        assert "Bob" in out


# ---------------------------------------------------------------------------
# Tests for add_trainer
# ---------------------------------------------------------------------------

class TestAddTrainer:
    def test_add_trainer_saves(self, monkeypatch, capsys):
        saved = []
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda _, data: saved.extend(data))

        main.add_trainer(make_args(name="Coach Mike", experience=5))

        assert saved[0]["name"] == "Coach Mike"
        assert saved[0]["experience"] == 5

    def test_add_trainer_prints_confirmation(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.add_trainer(make_args(name="Coach Mike", experience=5))
        assert "Coach Mike" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Tests for upgrade_membership
# ---------------------------------------------------------------------------

class TestUpgradeMembership:
    def _users(self):
        return [{"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "none"}]

    def _admin(self):
        return [{"id": 1, "user_id": 1, "trainer_id": 2, "schedule": "Mon 09:00", "status": "none"}]

    def test_upgrade_valid_plan(self, monkeypatch, capsys):
        users = self._users()
        admin = self._admin()
        monkeypatch.setattr(main, "load", lambda path: users if "users" in path else admin)
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.upgrade_membership(make_args(user_id=1, plan="gold"))
        assert users[0]["membership_plan"] == "gold"
        assert "gold" in capsys.readouterr().out

    def test_upgrade_invalid_user(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.upgrade_membership(make_args(user_id=99, plan="silver"))
        assert "not found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Tests for cancel_membership
# ---------------------------------------------------------------------------

class TestCancelMembership:
    def test_cancel_sets_none(self, monkeypatch, capsys):
        users = [{"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "gold"}]
        admin = [{"id": 1, "user_id": 1, "trainer_id": 2, "schedule": "Mon", "status": "gold"}]
        monkeypatch.setattr(main, "load", lambda path: users if "users" in path else admin)
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.cancel_membership(make_args(user_id=1))
        assert users[0]["membership_plan"] == "none"
        assert "cancelled" in capsys.readouterr().out

    def test_cancel_unknown_user(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.cancel_membership(make_args(user_id=42))
        assert "not found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Tests for book_trainer
# ---------------------------------------------------------------------------

class TestBookTrainer:
    def _data(self):
        users    = [{"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "gold"}]
        trainers = [{"id": 2, "name": "Coach Mike", "experience": 5, "trainees_id": []}]
        admin    = []
        return users, trainers, admin

    def test_book_trainer_creates_record(self, monkeypatch, capsys):
        users, trainers, admin = self._data()

        def fake_load(path):
            if "users"    in path: return users
            if "trainers" in path: return trainers
            return admin

        monkeypatch.setattr(main, "load", fake_load)
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.book_trainer(make_args(user_id=1, trainer_id=2, schedule="Mon 09:00"))
        assert 1 in trainers[0]["trainees_id"]
        assert "Alice" in capsys.readouterr().out

    def test_book_trainer_unknown_user(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.book_trainer(make_args(user_id=99, trainer_id=2, schedule="Mon 09:00"))
        assert "not found" in capsys.readouterr().out

    def test_book_trainer_unknown_trainer(self, monkeypatch, capsys):
        users = [{"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "gold"}]

        def fake_load(path):
            if "users" in path: return users
            return []

        monkeypatch.setattr(main, "load", fake_load)
        monkeypatch.setattr(main, "save", lambda *_: None)

        main.book_trainer(make_args(user_id=1, trainer_id=99, schedule="Mon 09:00"))
        assert "not found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Tests for list_schedules
# ---------------------------------------------------------------------------

class TestListSchedules:
    def test_list_schedules_empty(self, monkeypatch, capsys):
        monkeypatch.setattr(main, "load", lambda _: [])
        main.list_schedules(make_args())
        assert "No bookings" in capsys.readouterr().out

    def test_list_schedules_shows_entries(self, monkeypatch, capsys):
        admin    = [{"id": 1, "user_id": 1, "trainer_id": 2, "schedule": "Mon 09:00", "status": "gold"}]
        users    = [{"id": 1, "name": "Alice", "email": "a@a.com", "membership_plan": "gold"}]
        trainers = [{"id": 2, "name": "Coach Mike", "experience": 5, "trainees_id": [1]}]

        def fake_load(path):
            if "admin"    in path: return admin
            if "users"    in path: return users
            if "trainers" in path: return trainers
            return []

        monkeypatch.setattr(main, "load", fake_load)
        main.list_schedules(make_args())
        out = capsys.readouterr().out
        assert "Alice" in out
        assert "Coach Mike" in out
        assert "Mon 09:00" in out


# ---------------------------------------------------------------------------
# Tests for helper: next_id
# ---------------------------------------------------------------------------

class TestNextId:
    def test_empty_list_returns_1(self):
        assert main.next_id([]) == 1

    def test_increments_max(self):
        records = [{"id": 3}, {"id": 1}, {"id": 5}]
        assert main.next_id(records) == 6