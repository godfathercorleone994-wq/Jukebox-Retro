#!/usr/bin/env python3
"""
Tests for payment system and administrative features
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import uuid
from models import (
    DataStore, User, Transaction, UsageRecord, CashRegister,
    PaymentMethod, UserRole
)


class TestDataStore(unittest.TestCase):
    """Test DataStore functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.data_store = DataStore(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_initialize_default_admin(self):
        """Test that default admin is created"""
        admin = self.data_store.get_user("admin")
        self.assertIsNotNone(admin)
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.role, UserRole.ADMIN.value)
        self.assertTrue(admin.is_admin())
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "test123"
        hashed = self.data_store._hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(self.data_store.verify_password(password, hashed))
        self.assertFalse(self.data_store.verify_password("wrong", hashed))
    
    def test_create_and_get_user(self):
        """Test creating and retrieving a user"""
        user = User(
            username="testuser",
            password_hash=self.data_store._hash_password("password"),
            role=UserRole.USER.value,
            credits=10.0
        )
        self.data_store.update_user(user)
        
        retrieved = self.data_store.get_user("testuser")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.username, "testuser")
        self.assertEqual(retrieved.credits, 10.0)
        self.assertFalse(retrieved.is_admin())
    
    def test_update_user_credits(self):
        """Test updating user credits"""
        user = self.data_store.get_user("admin")
        original_credits = user.credits
        
        user.credits += 50.0
        self.data_store.update_user(user)
        
        updated = self.data_store.get_user("admin")
        self.assertEqual(updated.credits, original_credits + 50.0)


class TestTransactions(unittest.TestCase):
    """Test transaction functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.data_store = DataStore(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_add_transaction(self):
        """Test adding a transaction"""
        transaction = Transaction(
            transaction_id=str(uuid.uuid4()),
            username="admin",
            payment_method=PaymentMethod.PIX.value,
            amount=5.0,
            description="Test transaction"
        )
        
        self.data_store.add_transaction(transaction)
        transactions = self.data_store.load_transactions()
        
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].username, "admin")
        self.assertEqual(transactions[0].amount, 5.0)
        self.assertEqual(transactions[0].payment_method, PaymentMethod.PIX.value)
    
    def test_multiple_transactions(self):
        """Test adding multiple transactions"""
        for i in range(5):
            transaction = Transaction(
                transaction_id=str(uuid.uuid4()),
                username="admin",
                payment_method=PaymentMethod.CASH.value,
                amount=float(i + 1),
                description=f"Transaction {i}"
            )
            self.data_store.add_transaction(transaction)
        
        transactions = self.data_store.load_transactions()
        self.assertEqual(len(transactions), 5)


class TestUsageRecords(unittest.TestCase):
    """Test usage records functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.data_store = DataStore(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_add_usage_record(self):
        """Test adding a usage record"""
        record = UsageRecord(
            record_id=str(uuid.uuid4()),
            username="admin",
            song_title="Test Song",
            song_artist="Test Artist",
            payment_method=PaymentMethod.CREDITS.value,
            cost=1.0
        )
        
        self.data_store.add_usage_record(record)
        records = self.data_store.load_usage_records()
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].song_title, "Test Song")
        self.assertEqual(records[0].song_artist, "Test Artist")
    
    def test_usage_statistics(self):
        """Test calculating usage statistics"""
        # Add multiple records
        songs = [
            ("Song A", "Artist 1"),
            ("Song B", "Artist 2"),
            ("Song A", "Artist 1"),  # Duplicate
        ]
        
        for title, artist in songs:
            record = UsageRecord(
                record_id=str(uuid.uuid4()),
                username="admin",
                song_title=title,
                song_artist=artist,
                payment_method=PaymentMethod.PIX.value,
                cost=1.0
            )
            self.data_store.add_usage_record(record)
        
        records = self.data_store.load_usage_records()
        self.assertEqual(len(records), 3)
        
        # Count songs
        song_counts = {}
        for record in records:
            key = f"{record.song_artist} - {record.song_title}"
            song_counts[key] = song_counts.get(key, 0) + 1
        
        self.assertEqual(song_counts["Artist 1 - Song A"], 2)
        self.assertEqual(song_counts["Artist 2 - Song B"], 1)


class TestCashRegister(unittest.TestCase):
    """Test cash register functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.data_store = DataStore(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def test_add_cash_entry(self):
        """Test adding a cash register entry"""
        entry = CashRegister(
            entry_id=str(uuid.uuid4()),
            entry_type="income",
            amount=10.0,
            payment_method=PaymentMethod.CASH.value,
            description="Test income"
        )
        
        self.data_store.add_cash_register_entry(entry)
        entries = self.data_store.load_cash_register()
        
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].amount, 10.0)
        self.assertEqual(entries[0].entry_type, "income")
    
    def test_cash_balance_calculation(self):
        """Test calculating cash balance"""
        # Add income entries
        for i in range(3):
            entry = CashRegister(
                entry_id=str(uuid.uuid4()),
                entry_type="income",
                amount=10.0,
                payment_method=PaymentMethod.PIX.value,
                description=f"Income {i}"
            )
            self.data_store.add_cash_register_entry(entry)
        
        # Add expense entry
        entry = CashRegister(
            entry_id=str(uuid.uuid4()),
            entry_type="expense",
            amount=5.0,
            payment_method=PaymentMethod.PIX.value,
            description="Expense"
        )
        self.data_store.add_cash_register_entry(entry)
        
        balance = self.data_store.get_cash_balance()
        
        # 3 * 10.0 - 5.0 = 25.0
        self.assertEqual(balance[PaymentMethod.PIX.value], 25.0)
        self.assertEqual(balance["total"], 25.0)
    
    def test_multiple_payment_methods_balance(self):
        """Test balance calculation with multiple payment methods"""
        methods = [
            PaymentMethod.PIX.value,
            PaymentMethod.CASH.value,
            PaymentMethod.DEBIT.value,
            PaymentMethod.CREDIT.value
        ]
        
        for method in methods:
            entry = CashRegister(
                entry_id=str(uuid.uuid4()),
                entry_type="income",
                amount=100.0,
                payment_method=method,
                description=f"Income via {method}"
            )
            self.data_store.add_cash_register_entry(entry)
        
        balance = self.data_store.get_cash_balance()
        
        for method in methods:
            self.assertEqual(balance[method], 100.0)
        
        self.assertEqual(balance["total"], 400.0)


class TestPaymentMethods(unittest.TestCase):
    """Test payment method enums"""
    
    def test_payment_method_values(self):
        """Test payment method enum values"""
        self.assertEqual(PaymentMethod.PIX.value, "pix")
        self.assertEqual(PaymentMethod.CASH.value, "dinheiro")
        self.assertEqual(PaymentMethod.DEBIT.value, "débito")
        self.assertEqual(PaymentMethod.CREDIT.value, "crédito")
        self.assertEqual(PaymentMethod.CREDITS.value, "créditos")
        self.assertEqual(PaymentMethod.ADMIN_FREE.value, "admin_free")
    
    def test_user_role_values(self):
        """Test user role enum values"""
        self.assertEqual(UserRole.ADMIN.value, "admin")
        self.assertEqual(UserRole.USER.value, "user")


class TestUserModel(unittest.TestCase):
    """Test User model"""
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User(
            username="testuser",
            password_hash="hashed_password",
            role=UserRole.USER.value,
            credits=0.0
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertFalse(user.is_admin())
        self.assertIsNotNone(user.created_at)
    
    def test_admin_user(self):
        """Test admin user"""
        admin = User(
            username="admin",
            password_hash="hashed_password",
            role=UserRole.ADMIN.value,
            credits=1000.0
        )
        
        self.assertTrue(admin.is_admin())
    
    def test_user_to_dict(self):
        """Test converting user to dictionary"""
        user = User(
            username="testuser",
            password_hash="hashed_password",
            role=UserRole.USER.value,
            credits=10.0
        )
        
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['credits'], 10.0)
        self.assertIn('created_at', user_dict)


if __name__ == '__main__':
    print("Running payment system tests...\n")
    unittest.main(verbosity=2)
