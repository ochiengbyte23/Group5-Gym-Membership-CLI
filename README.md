# 🏋️ Gym Membership CLI

A command-line application for managing gym memberships, trainers, and session bookings. Built with Python using object-oriented design and JSON-based data persistence.

---

## Project Structure

```
gym-cli/
├── main.py               # Entry point & CLI command definitions
├── Pipfile               # Pipenv dependency manager
├── Pipfile.lock
├── requirements.txt
├── README.md
│
├── lib/                  # Core models
│   ├── Admin.py          # Booking/scheduling model
│   ├── Membership.py     # Membership plans & pricing
│   ├── Trainer.py        # Trainer model
│   ├── User.py           # User model
│   └── testing/          # Test suite
│       └── test_gym.py
│
├── models/               # (reserved for future model extensions)
│
└── data/                 # Auto-generated JSON storage
    ├── admin.json
    ├── trainers.json
    └── users.json
```

---

## Setup

**Requirements:** Python 3.7+

### Using Pipenv (recommended)

```bash
git clone <your-repo-url>
cd gym-cli
pipenv install
pipenv shell
```

### Using pip

```bash
pip install -r requirements.txt
```

---

## Usage

All commands follow the pattern:

```bash
python main.py <command> [arguments]
```

---

### 👤 Users

| Command | Arguments | Description |
| --- | --- | --- |
| `add-user` | `name email` | Register a new user |
| `list-users` | — | Display all users |

```bash
python main.py add-user "Jane Doe" jane@example.com
python main.py list-users
```

---

### 🏅 Memberships

| Command | Arguments | Description |
| --- | --- | --- |
| `upgrade-membership` | `user_id plan` | Assign or upgrade a plan |
| `cancel-membership` | `user_id` | Cancel a user's active plan |

```bash
python main.py upgrade-membership 1 gold
python main.py cancel-membership 1
```

**Available plans:**

| Plan    | Duration   | Price (Ksh) |
|---------|------------|-------------|
| bronze  | 1 month    | 5,000       |
| silver  | 3 months   | 8,000       |
| gold    | 6 months   | 15,000      |
| diamond | 12 months  | 30,000      |

---

### 🧑‍🏫 Trainers

| Command | Arguments | Description |
| --- | --- | --- |
| `add-trainer` | `name experience` | Register a new trainer |
| `list-trainers` | — | Display all trainers |

```bash
python main.py add-trainer "Mike Smith" 5
python main.py list-trainers
```

---

### 📅 Bookings

| Command | Arguments | Description |
| --- | --- | --- |
| `book-trainer` | `user_id trainer_id schedule` | Book a session |
| `list-schedules` | — | View all bookings |

```bash
python main.py book-trainer 1 2 "Mon 09:00"
python main.py list-schedules
```

---

## Running Tests

```bash
# From the project root
python -m pytest lib/testing/test_gym.py -v
```

Test coverage includes unit tests for all four models (`User`, `Trainer`, `Membership`, `Admin`) and integration tests for every CLI command.

---

## Data Storage

All records are persisted as JSON in the `data/` directory, created automatically on first run. IDs auto-increment based on the highest existing record.

---

## Example Workflow

```bash
# 1. Add a user and a trainer
python main.py add-user "Alice" alice@gym.com
python main.py add-trainer "Bob" 7

# 2. Assign a membership
python main.py upgrade-membership 1 gold

# 3. Book a session
python main.py book-trainer 1 1 "Wed 07:00"

# 4. Review the schedule
python main.py list-schedules
```
