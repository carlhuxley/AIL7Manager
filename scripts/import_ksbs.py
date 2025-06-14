
import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.postgres_models import Base, KSB

def parse_ksb_file(file_path: str) -> tuple[str, str]:
    """Parse a KSB markdown file to extract code and description"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract KSB code from filename (e.g., K1.md -> K1)
    filename = os.path.basename(file_path)
    ksb_code = os.path.splitext(filename)[0]
    
    # Use the entire content as description, or parse if there's a specific format
    description = content.strip()
    
    return ksb_code, description

def import_ksbs_from_directory(directory_path: str, database_url: str):
    """Import all KSB markdown files from a directory"""
    
    # Setup database
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        imported_count = 0
        skipped_count = 0
        
        # Process all .md files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.md'):
                file_path = os.path.join(directory_path, filename)
                
                try:
                    ksb_code, description = parse_ksb_file(file_path)
                    
                    # Check if KSB already exists
                    existing_ksb = db.query(KSB).filter(KSB.code == ksb_code).first()
                    if existing_ksb:
                        print(f"Skipping {ksb_code} - already exists")
                        skipped_count += 1
                        continue
                    
                    # Create new KSB
                    new_ksb = KSB(code=ksb_code, description=description)
                    db.add(new_ksb)
                    db.commit()
                    
                    print(f"Imported KSB: {ksb_code}")
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    db.rollback()
        
        print(f"\nImport complete:")
        print(f"  Imported: {imported_count} KSBs")
        print(f"  Skipped: {skipped_count} KSBs")
        
    finally:
        db.close()

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python import_ksbs.py <directory_path> <database_url>")
        print("Example: python import_ksbs.py ./ksbs postgresql://user:password@localhost/apprentice_hub")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    database_url = sys.argv[2]
    
    if not os.path.exists(directory_path):
        print(f"Error: Directory {directory_path} does not exist")
        sys.exit(1)
    
    import_ksbs_from_directory(directory_path, database_url)
