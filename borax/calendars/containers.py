# coding=utf8

import collections
import csv
from pathlib import Path
from typing import Union

from borax.calendars.festivals2 import MixedDate, decode


class FestivalLibrary(collections.UserList):
    def get_festival_names(self, date_obj: MixedDate) -> list:
        names = []
        for festival in self.data:
            if festival.is_(date_obj):
                names.append(festival.name)
        return names

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> 'FestivalLibrary':
        if isinstance(file_path, str):
            file_path = Path(file_path)
        fl = cls()
        field_names = ['raw', 'name']
        with file_path.open(encoding='utf8') as f:
            reader = csv.DictReader(f, fieldnames=field_names)
            for row in reader:
                try:
                    festival = decode(row['raw'])
                    festival.set_name(row['name'])
                    fl.append(festival)
                except ValueError:
                    continue
        return fl

    @classmethod
    def from_builtin(cls, identifier: str = 'zh-Hans') -> 'FestivalLibrary':
        file_dict = {
            'zh-Hans': 'FestivalData.txt'
        }
        file_path = Path(__file__).parent / file_dict.get(identifier)
        return cls.from_file(file_path)
