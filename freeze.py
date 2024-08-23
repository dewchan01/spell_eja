from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

def delete_audios_url_generator():
    return []  # No URLs to freeze for delete_audios

freezer.register_generator(delete_audios_url_generator)
if __name__ == '__main__':
    freezer.freeze()