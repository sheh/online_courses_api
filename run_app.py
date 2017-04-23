import argparse
import os
import tempfile

from online_courses_api import app
from online_courses_api.database import init_db

DEFAULT_DB_FILE_NAME = 'online_courses_api.db'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--drop-db', dest='drop_db', action='store_true')
    parser.add_argument('--db', default=os.path.join(tempfile.gettempdir(), DEFAULT_DB_FILE_NAME))

    args = parser.parse_args()
    print(f'Use database file {args.db}')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{args.db}'

    if args.drop_db:
        print(f'--drop-db set, removing file {args.db}')
        os.remove(args.db)

    if not os.path.exists(args.db):
        print(f'File {args.db} not found, create and init database')
        with app.app_context():
            init_db()
    app.run(port=args.port, debug=True)
