import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models.postgres_models import KSB, Base
from config import Settings

def import_ksbs_from_markdown(ksb_folder_path, db_url):
    """
    Imports KSBs from markdown files into the database.

    Args:
        ksb_folder_path (str): The path to the folder containing KSB markdown files.
        db_url (str): The database URL.
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    for filename in os.listdir(ksb_folder_path):
        if filename.endswith(".desc.md"):
            ksb_code = filename.split('.')[0].upper()
            filepath = os.path.join(ksb_folder_path, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                description = f.read().strip()

            # Check if the KSB already exists
            existing_ksb = session.query(KSB).filter_by(code=ksb_code).first()
            if existing_ksb:
                print(f"KSB {ksb_code} already exists, skipping.")
                continue

            new_ksb = KSB(code=ksb_code, description=description)
            session.add(new_ksb)
            print(f"Adding KSB: {ksb_code}")

    session.commit()
    session.close()
    print("KSB import complete.")

if __name__ == "__main__":
    settings = Settings()
    ksb_folder = "ksbs"
    import_ksbs_from_markdown(ksb_folder, settings.postgres_url)