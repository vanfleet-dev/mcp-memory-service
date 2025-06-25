#!/usr/bin/env python3
"""
Migration script to clean up timestamp mess in MCP Memory ChromaDB database.
This script will:
1. Backup the database
2. Standardize timestamps to use only the 'timestamp' field as integer
3. Remove redundant timestamp fields
4. Ensure all memories have proper timestamps
"""

import sqlite3
import shutil
import os
from datetime import datetime
import sys

# Database paths
DB_PATH = "/Users/hkr/Library/Application Support/mcp-memory/chroma_db/chroma.sqlite3"
BACKUP_PATH = f"{DB_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def backup_database():
    """Create a backup of the database before migration."""
    print(f"Creating backup at: {BACKUP_PATH}")
    try:
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print("✅ Backup created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return False

def analyze_timestamps(conn):
    """Analyze current timestamp situation."""
    print("\n📊 Analyzing current timestamp fields...")
    
    cursor = conn.cursor()
    
    # Get all unique timestamp-related keys
    cursor.execute("""
        SELECT key, 
               COUNT(DISTINCT id) as memory_count,
               COUNT(CASE WHEN string_value IS NOT NULL THEN 1 END) as string_values,
               COUNT(CASE WHEN int_value IS NOT NULL THEN 1 END) as int_values,
               COUNT(CASE WHEN float_value IS NOT NULL THEN 1 END) as float_values
        FROM embedding_metadata
        WHERE key IN ('timestamp', 'created_at', 'created_at_iso', 'timestamp_float', 
                      'timestamp_str', 'updated_at', 'updated_at_iso', 'date')
        GROUP BY key
        ORDER BY key
    """)
    
    results = cursor.fetchall()
    print("\nTimestamp field usage:")
    print("-" * 70)
    print(f"{'Field':<20} {'Memories':<12} {'String':<10} {'Int':<10} {'Float':<10}")
    print("-" * 70)
    
    for row in results:
        print(f"{row[0]:<20} {row[1]:<12} {row[2]:<10} {row[3]:<10} {row[4]:<10}")
    
    return results

def migrate_timestamps(conn):
    """Migrate all timestamps to standardized format."""
    print("\n🔄 Starting timestamp migration...")
    
    cursor = conn.cursor()
    
    # First, ensure all memories have a timestamp value
    # Priority: timestamp (int) > created_at (float) > timestamp_float (float)
    
    print("Step 1: Ensuring all memories have timestamp values...")
    
    # Count memories without any timestamp
    cursor.execute("""
        SELECT COUNT(DISTINCT em.id)
        FROM embedding_metadata em
        WHERE em.id NOT IN (
            SELECT id FROM embedding_metadata 
            WHERE key = 'timestamp' AND int_value IS NOT NULL
        )
    """)
    
    missing_count = cursor.fetchone()[0]
    print(f"  Found {missing_count} memories without integer timestamp")
    
    if missing_count > 0:
        # Get memories that need timestamp migration
        cursor.execute("""
            SELECT DISTINCT 
                em.id,
                MAX(CASE WHEN em2.key = 'created_at' THEN em2.float_value END) as created_at_float,
                MAX(CASE WHEN em2.key = 'timestamp_float' THEN em2.float_value END) as timestamp_float
            FROM embedding_metadata em
            LEFT JOIN embedding_metadata em2 ON em.id = em2.id 
                AND em2.key IN ('created_at', 'timestamp_float')
            WHERE em.id NOT IN (
                SELECT id FROM embedding_metadata 
                WHERE key = 'timestamp' AND int_value IS NOT NULL
            )
            GROUP BY em.id
        """)
        
        memories_to_fix = cursor.fetchall()
        fixed_count = 0
        
        for memory_id, created_at, timestamp_float in memories_to_fix:
            # Use the first available timestamp
            timestamp_value = None
            if created_at:
                timestamp_value = int(created_at)
            elif timestamp_float:
                timestamp_value = int(timestamp_float)
            else:
                # If no timestamp found, use current time (this shouldn't happen)
                timestamp_value = int(datetime.now().timestamp())
                print(f"  ⚠️  Memory {memory_id} has no timestamp, using current time")
            
            # Insert the timestamp value
            cursor.execute("""
                INSERT INTO embedding_metadata (id, key, string_value, int_value, float_value)
                VALUES (?, 'timestamp', NULL, ?, NULL)
            """, (memory_id, timestamp_value))
            
            fixed_count += 1
        
        conn.commit()
        print(f"  ✅ Fixed {fixed_count} memories with missing timestamps")
    
    # Step 2: Update existing timestamp fields that have wrong data type
    print("\nStep 2: Standardizing timestamp data types...")
    
    # Find timestamps stored as floats that should be ints
    cursor.execute("""
        UPDATE embedding_metadata
        SET int_value = CAST(float_value AS INTEGER),
            float_value = NULL
        WHERE key = 'timestamp' 
        AND float_value IS NOT NULL 
        AND int_value IS NULL
    """)
    
    float_fixes = cursor.rowcount
    conn.commit()
    print(f"  ✅ Converted {float_fixes} float timestamps to integers")

def cleanup_redundant_fields(conn):
    """Remove redundant timestamp fields."""
    print("\n🧹 Cleaning up redundant timestamp fields...")
    
    cursor = conn.cursor()
    
    # List of redundant fields to remove
    redundant_fields = [
        'created_at', 'created_at_iso', 'timestamp_float', 
        'timestamp_str', 'updated_at', 'updated_at_iso', 'date'
    ]
    
    total_deleted = 0
    
    for field in redundant_fields:
        cursor.execute("""
            DELETE FROM embedding_metadata
            WHERE key = ?
        """, (field,))
        
        deleted = cursor.rowcount
        total_deleted += deleted
        
        if deleted > 0:
            print(f"  ✅ Removed {deleted} '{field}' entries")
    
    conn.commit()
    print(f"\n  Total redundant entries removed: {total_deleted}")

def verify_migration(conn):
    """Verify the migration was successful."""
    print("\n✔️  Verifying migration results...")
    
    cursor = conn.cursor()
    
    # Check that all memories have timestamps
    cursor.execute("""
        SELECT COUNT(DISTINCT e.id)
        FROM embeddings e
        LEFT JOIN embedding_metadata em 
            ON e.id = em.id AND em.key = 'timestamp'
        WHERE em.int_value IS NULL
    """)
    
    missing = cursor.fetchone()[0]
    
    if missing > 0:
        print(f"  ⚠️  WARNING: {missing} memories still missing timestamps")
    else:
        print("  ✅ All memories have timestamps")
    
    # Check for any remaining redundant fields
    cursor.execute("""
        SELECT key, COUNT(*) as count
        FROM embedding_metadata
        WHERE key IN ('created_at', 'created_at_iso', 'timestamp_float', 
                      'timestamp_str', 'updated_at', 'updated_at_iso', 'date')
        GROUP BY key
    """)
    
    redundant = cursor.fetchall()
    
    if redundant:
        print("  ⚠️  WARNING: Found remaining redundant fields:")
        for field, count in redundant:
            print(f"     - {field}: {count} entries")
    else:
        print("  ✅ All redundant timestamp fields removed")
    
    # Show final timestamp field stats
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT id) as total_memories,
            COUNT(CASE WHEN int_value IS NOT NULL THEN 1 END) as valid_timestamps,
            MIN(int_value) as earliest_timestamp,
            MAX(int_value) as latest_timestamp
        FROM embedding_metadata
        WHERE key = 'timestamp'
    """)
    
    stats = cursor.fetchone()
    
    print(f"\n📊 Final Statistics:")
    print(f"  Total memories with timestamps: {stats[0]}")
    print(f"  Valid integer timestamps: {stats[1]}")
    
    if stats[2] and stats[3]:
        earliest = datetime.fromtimestamp(stats[2]).strftime('%Y-%m-%d %H:%M:%S')
        latest = datetime.fromtimestamp(stats[3]).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  Date range: {earliest} to {latest}")

def main():
    """Main migration function."""
    print("=" * 70)
    print("MCP Memory Timestamp Migration Script")
    print("=" * 70)
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        return 1
    
    # Create backup
    if not backup_database():
        print("❌ Migration aborted - could not create backup")
        return 1
    
    # Connect to database
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"\n✅ Connected to database: {DB_PATH}")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return 1
    
    try:
        # Analyze current state
        analyze_timestamps(conn)
        
        # Ask for confirmation
        print("\n" + "=" * 70)
        print("⚠️  This migration will:")
        print("  1. Standardize all timestamps to integer format in 'timestamp' field")
        print("  2. Remove all redundant timestamp fields")
        print("  3. Ensure all memories have valid timestamps")
        print("\nA backup has been created at:")
        print(f"  {BACKUP_PATH}")
        print("=" * 70)
        
        response = input("\nProceed with migration? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("Migration cancelled.")
            conn.close()
            return 0
        
        # Perform migration
        migrate_timestamps(conn)
        cleanup_redundant_fields(conn)
        
        # Verify results
        verify_migration(conn)
        
        # Vacuum database to reclaim space
        print("\n🔧 Optimizing database...")
        conn.execute("VACUUM")
        conn.commit()
        print("  ✅ Database optimized")
        
        print("\n✅ Migration completed successfully!")
        print(f"\nBackup saved at: {BACKUP_PATH}")
        print("You can restore the backup if needed by copying it back to the original location.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("Rolling back changes...")
        conn.rollback()
        print(f"Please restore from backup: {BACKUP_PATH}")
        return 1
    finally:
        conn.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
