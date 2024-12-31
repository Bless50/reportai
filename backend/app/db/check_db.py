from sqlalchemy import text, inspect
from app.db.session import engine

def check_db():
    # Get inspector
    inspector = inspect(engine)
    
    # Check sections table
    print("\n=== SECTIONS TABLE STRUCTURE ===")
    columns = inspector.get_columns('sections')
    for col in columns:
        print(f"Column: {col['name']}, Type: {col['type']}, Nullable: {col['nullable']}")
    
    # Check data in sections
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) from sections"))
        count = result.scalar()
        print(f"\nTotal sections: {count}")
        
        # Sample some data
        print("\n=== SAMPLE SECTION DATA ===")
        result = conn.execute(text("SELECT * FROM sections LIMIT 3"))
        for row in result:
            print(row)

if __name__ == "__main__":
    check_db()
