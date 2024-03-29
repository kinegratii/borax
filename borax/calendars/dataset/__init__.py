from pathlib import Path

__all__ = ['get_festival_dataset_path']

_FILE_DICT = {
    'basic': 'FestivalData.csv',
    'ext1': 'festivals_ext1.csv',
    'zh-Hans': 'FestivalData.csv'
}


def get_festival_dataset_path(identifier: str) -> Path:
    """Return the full path for festival dataset csv file."""
    if identifier not in _FILE_DICT:
        raise ValueError(f'Festival Dataset {identifier} not found!')
    return Path(__file__).parent / _FILE_DICT.get(identifier)
