#!/usr/bin/env python3
"""
Data models for Jukebox Retro payment and administration system
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
import json
from pathlib import Path
from enum import Enum


class PaymentMethod(Enum):
    """Payment method types"""
    PIX = "pix"
    CASH = "dinheiro"
    DEBIT = "débito"
    CREDIT = "crédito"
    CREDITS = "créditos"  # Internal credits system
    ADMIN_FREE = "admin_free"  # Admin adding credits for free


class UserRole(Enum):
    """User role types"""
    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    """User model"""
    username: str
    password_hash: str
    role: str  # "admin" or "user"
    credits: float = 0.0
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN.value
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Transaction:
    """Transaction model for payments"""
    transaction_id: str
    username: str
    payment_method: str
    amount: float
    description: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)


@dataclass
class UsageRecord:
    """Usage statistics record"""
    record_id: str
    username: str
    song_title: str
    song_artist: str
    played_at: str = None
    payment_method: str = None
    cost: float = 0.0
    
    def __post_init__(self):
        if self.played_at is None:
            self.played_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)


@dataclass
class CashRegister:
    """Cash register for tracking income and expenses"""
    entry_id: str
    entry_type: str  # "income" or "expense"
    amount: float
    payment_method: str
    description: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)


class DataStore:
    """Data storage manager for all application data"""
    
    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path.home() / ".jukebox_retro"
        
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.users_file = self.data_dir / "users.json"
        self.transactions_file = self.data_dir / "transactions.json"
        self.usage_file = self.data_dir / "usage_stats.json"
        self.cash_register_file = self.data_dir / "cash_register.json"
        
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize data files if they don't exist"""
        if not self.users_file.exists():
            # Create default admin user
            default_admin = User(
                username="admin",
                password_hash=self._hash_password("admin123"),
                role=UserRole.ADMIN.value,
                credits=1000.0
            )
            self.save_users([default_admin])
        
        if not self.transactions_file.exists():
            self.save_transactions([])
        
        if not self.usage_file.exists():
            self.save_usage_records([])
        
        if not self.cash_register_file.exists():
            self.save_cash_register([])
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing (in production, use bcrypt or similar)"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    # Users
    def load_users(self) -> List[User]:
        """Load users from file"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [User(**u) for u in data]
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
    
    def save_users(self, users: List[User]):
        """Save users to file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump([u.to_dict() for u in users], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None
    
    def update_user(self, user: User):
        """Update user information"""
        users = self.load_users()
        for i, u in enumerate(users):
            if u.username == user.username:
                users[i] = user
                break
        else:
            users.append(user)
        self.save_users(users)
    
    # Transactions
    def load_transactions(self) -> List[Transaction]:
        """Load transactions from file"""
        try:
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Transaction(**t) for t in data]
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return []
    
    def save_transactions(self, transactions: List[Transaction]):
        """Save transactions to file"""
        try:
            with open(self.transactions_file, 'w', encoding='utf-8') as f:
                json.dump([t.to_dict() for t in transactions], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def add_transaction(self, transaction: Transaction):
        """Add a new transaction"""
        transactions = self.load_transactions()
        transactions.append(transaction)
        self.save_transactions(transactions)
    
    # Usage Records
    def load_usage_records(self) -> List[UsageRecord]:
        """Load usage records from file"""
        try:
            with open(self.usage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [UsageRecord(**r) for r in data]
        except Exception as e:
            print(f"Error loading usage records: {e}")
            return []
    
    def save_usage_records(self, records: List[UsageRecord]):
        """Save usage records to file"""
        try:
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump([r.to_dict() for r in records], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving usage records: {e}")
    
    def add_usage_record(self, record: UsageRecord):
        """Add a new usage record"""
        records = self.load_usage_records()
        records.append(record)
        self.save_usage_records(records)
    
    # Cash Register
    def load_cash_register(self) -> List[CashRegister]:
        """Load cash register entries from file"""
        try:
            with open(self.cash_register_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [CashRegister(**e) for e in data]
        except Exception as e:
            print(f"Error loading cash register: {e}")
            return []
    
    def save_cash_register(self, entries: List[CashRegister]):
        """Save cash register entries to file"""
        try:
            with open(self.cash_register_file, 'w', encoding='utf-8') as f:
                json.dump([e.to_dict() for e in entries], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving cash register: {e}")
    
    def add_cash_register_entry(self, entry: CashRegister):
        """Add a new cash register entry"""
        entries = self.load_cash_register()
        entries.append(entry)
        self.save_cash_register(entries)
    
    def get_cash_balance(self) -> dict:
        """Calculate cash register balance by payment method"""
        entries = self.load_cash_register()
        balance = {
            PaymentMethod.PIX.value: 0.0,
            PaymentMethod.CASH.value: 0.0,
            PaymentMethod.DEBIT.value: 0.0,
            PaymentMethod.CREDIT.value: 0.0,
            "total": 0.0
        }
        
        for entry in entries:
            amount = entry.amount if entry.entry_type == "income" else -entry.amount
            if entry.payment_method in balance:
                balance[entry.payment_method] += amount
            balance["total"] += amount
        
        return balance
