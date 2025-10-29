#!/usr/bin/env python3
"""
Demo script to showcase the payment system functionality
This demonstrates the core payment system features without the GUI
"""

import tempfile
import shutil
from pathlib import Path
import uuid
from models import (
    DataStore, User, Transaction, UsageRecord, CashRegister,
    PaymentMethod, UserRole
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def demo_payment_system():
    """Demonstrate the payment system features"""
    
    # Create temporary data store for demo
    temp_dir = Path(tempfile.mkdtemp())
    data_store = DataStore(data_dir=temp_dir)
    
    print("\n🎵 JUKEBOX RETRO - PAYMENT SYSTEM DEMO 🎵\n")
    
    # 1. Show default admin user
    print_section("1. Default Admin User")
    admin = data_store.get_user("admin")
    print(f"Username: {admin.username}")
    print(f"Role: {admin.role}")
    print(f"Is Admin: {admin.is_admin()}")
    print(f"Credits: R$ {admin.credits:.2f}")
    
    # 2. Create a regular user
    print_section("2. Creating a Regular User")
    new_user = User(
        username="joao",
        password_hash=data_store._hash_password("senha123"),
        role=UserRole.USER.value,
        credits=0.0
    )
    data_store.update_user(new_user)
    print(f"Created user: {new_user.username}")
    print(f"Role: {new_user.role}")
    print(f"Initial credits: R$ {new_user.credits:.2f}")
    
    # 3. User adds credits via PIX
    print_section("3. User Adds Credits (PIX Payment)")
    amount = 50.0
    new_user.credits += amount
    data_store.update_user(new_user)
    
    # Record transaction
    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        username=new_user.username,
        payment_method=PaymentMethod.PIX.value,
        amount=amount,
        description="Recarga de créditos"
    )
    data_store.add_transaction(transaction)
    
    # Record cash register entry
    cash_entry = CashRegister(
        entry_id=str(uuid.uuid4()),
        entry_type="income",
        amount=amount,
        payment_method=PaymentMethod.PIX.value,
        description="Recarga de créditos - joao"
    )
    data_store.add_cash_register_entry(cash_entry)
    
    print(f"Added R$ {amount:.2f} via {PaymentMethod.PIX.value}")
    print(f"New balance: R$ {new_user.credits:.2f}")
    
    # 4. User plays songs
    print_section("4. User Plays Songs")
    songs = [
        ("Bohemian Rhapsody", "Queen"),
        ("Stairway to Heaven", "Led Zeppelin"),
        ("Hotel California", "Eagles"),
    ]
    
    song_cost = 1.0
    for title, artist in songs:
        # Deduct cost
        new_user.credits -= song_cost
        data_store.update_user(new_user)
        
        # Record usage
        usage_record = UsageRecord(
            record_id=str(uuid.uuid4()),
            username=new_user.username,
            song_title=title,
            song_artist=artist,
            payment_method=PaymentMethod.CREDITS.value,
            cost=song_cost
        )
        data_store.add_usage_record(usage_record)
        
        print(f"♪ Played: {artist} - {title} (R$ {song_cost:.2f})")
    
    print(f"Remaining credits: R$ {new_user.credits:.2f}")
    
    # 5. Admin adds credits for free
    print_section("5. Admin Adds Credits (Free)")
    admin.credits += 100.0
    data_store.update_user(admin)
    
    # Record transaction (but not in cash register)
    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        username=admin.username,
        payment_method="admin_free",
        amount=100.0,
        description="Admin free credits"
    )
    data_store.add_transaction(transaction)
    
    print(f"Admin added R$ 100.00 for free")
    print(f"Admin new balance: R$ {admin.credits:.2f}")
    
    # 6. Show statistics
    print_section("6. Usage Statistics")
    usage_records = data_store.load_usage_records()
    transactions = data_store.load_transactions()
    
    print(f"Total songs played: {len(usage_records)}")
    print(f"Total transactions: {len(transactions)}")
    print(f"Total revenue: R$ {sum(r.cost for r in usage_records):.2f}")
    
    # Payment method breakdown
    payment_methods = {}
    for record in usage_records:
        pm = record.payment_method
        payment_methods[pm] = payment_methods.get(pm, 0) + 1
    
    print("\nPayment methods used:")
    for method, count in payment_methods.items():
        print(f"  - {method}: {count} songs")
    
    # 7. Cash register balance
    print_section("7. Cash Register Balance")
    balance = data_store.get_cash_balance()
    
    print(f"Total: R$ {balance['total']:.2f}")
    print("\nBy payment method:")
    for method in [PaymentMethod.PIX.value, PaymentMethod.CASH.value, 
                   PaymentMethod.DEBIT.value, PaymentMethod.CREDIT.value]:
        if balance.get(method, 0) != 0:
            print(f"  {method}: R$ {balance[method]:.2f}")
    
    # 8. All users
    print_section("8. All Users in System")
    users = data_store.load_users()
    for user in users:
        role_badge = "[ADMIN]" if user.is_admin() else "[USER]"
        print(f"{user.username} {role_badge} - Credits: R$ {user.credits:.2f}")
    
    # 9. Recent transactions
    print_section("9. Recent Transactions")
    recent_transactions = transactions[-5:]  # Last 5
    for trans in recent_transactions:
        print(f"{trans.username} | R$ {trans.amount:.2f} | {trans.payment_method} | {trans.description}")
    
    print("\n" + "="*60)
    print("  Demo completed successfully!")
    print("="*60 + "\n")
    
    # Cleanup
    shutil.rmtree(temp_dir)
    print("✓ Temporary data cleaned up\n")


if __name__ == "__main__":
    try:
        demo_payment_system()
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()
