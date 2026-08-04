from app.database.session import SessionLocal
from app.seed.master_seed import seed_master_data


def main():
    db = SessionLocal()

    try:
        seed_master_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()