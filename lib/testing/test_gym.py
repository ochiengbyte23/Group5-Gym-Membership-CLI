import pytest
from lib.User import User
from lib.Trainer import Trainer
from lib.Membership import Membership
from lib.Admin import Admin

# --- User Class Tests ---
def test_user_initialization():
    """Verify a user is created with correct default plan."""
    user = User(1, "Bill", "bill@email.com")
    assert user.name == "Bill"
    assert user.membership_plan == "none"

def test_user_to_dict():
    """Verify the dictionary conversion matches your JSON structure."""
    user = User(1, "Bill", "bill@email.com")
    expected = {
        "id": 1,
        "name": "Bill",
        "email": "bill@email.com",
        "membership_plan": "none",
    }
    assert user.to_dict() == expected

# --- Trainer Class Tests ---
def test_trainer_add_trainee():
    """Verify trainers can track unique user IDs."""
    trainer = Trainer(101, "Coach Sarah", 5)
    trainer.add_user_to_list(1)
    trainer.add_user_to_list(1)  # Duplicate check
    assert len(trainer.trainees_id) == 1
    assert 1 in trainer.trainees_id

# --- Membership Class Tests ---
def test_membership_pricing():
    """Verify the fixed pricing dictionary in the Membership class."""
    member = Membership()
    assert member.PLANS["gold"]["price"] == 15000
    
def test_membership_upgrade():
    """Verify a user can change their plan status."""
    member = Membership("none")
    member.plan_upgrade("diamond")
    assert member.membership_plan == "diamond"

# --- Admin (Booking) Class Tests ---
def test_admin_booking_creation():
    """Verify that a booking correctly links user and trainer."""
    # Note: Admin init appends to a class list 'admin_list'
    Admin.admin_list = [] # Reset list for clean test
    booking = Admin(
        admin_id=1, 
        schedule="Mon 10:00", 
        trainee_id=101, 
        user_id=1, 
        status="gold"
    )
    
    assert booking.admin_id == 1
    assert booking.no_members() == 1
    assert "Mon 10:00" in str(booking)