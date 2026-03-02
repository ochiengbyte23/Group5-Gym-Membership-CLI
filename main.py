import argparse
import os

from models.Admin import Admin
from models.Membership import Membership
from models.Trainer import Trainer
from models.User import User

#________file path using os and json__________
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
TRAINERS_FILE = os.path.join(DATA_DIR, 'trainers.json')
MEMBERSHIPS_FILE = os.path.join(DATA_DIR, 'memberships.json')
ADMIN_FILE = os.path.join(DATA_DIR, 'admin.json')

os.makedirs(DATA_DIR, exist_ok=True)

#___________User commands_________
def add_user(args):
    pass