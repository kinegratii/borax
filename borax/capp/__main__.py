from borax.capp.borax_calendar_app import start_calendar_app
from borax.capp.festival_creator import start_festival_creator

if __name__ == '__main__':
    import sys

    pro_args = sys.argv[1:]
    if 'creator' in pro_args:
        start_festival_creator()
    else:
        start_calendar_app()
