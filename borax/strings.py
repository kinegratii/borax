import re


def camel2snake(s: str) -> str:
    """Convert camel string to snake string.

    >>> camel2snake('Act')
    'act'
    >>> camel2snake('SnakeString')
    'snake_string'
    """
    camel_to_snake_regex = r'((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))'
    return re.sub(camel_to_snake_regex, r'_\1', s).lower()


def snake2camel(s: str) -> str:
    """Convert snake string to camel string.

    >>> snake2camel('snake_string')
    'SnakeString'
    >>> snake2camel('act')
    'Act'
    """
    snake_to_camel_regex = r"(?:^|_)(.)"
    return re.sub(snake_to_camel_regex, lambda m: m.group(1).upper(), s)


def get_percentage_display(value, places=2):
    fmt = '{:. %}'.replace(' ', str(places))
    return fmt.format(value)


class FileEndingUtil:
    WINDOWS_LINE_ENDING = b'\r\n'
    LINUX_LINE_ENDING = b'\n'

    @staticmethod
    def windows2linux(content: bytes) -> bytes:
        assert isinstance(content, bytes)
        return content.replace(FileEndingUtil.WINDOWS_LINE_ENDING, FileEndingUtil.LINUX_LINE_ENDING)

    @staticmethod
    def linux2windows(content: bytes) -> bytes:
        return content.replace(FileEndingUtil.LINUX_LINE_ENDING, FileEndingUtil.WINDOWS_LINE_ENDING)

    @staticmethod
    def convert_to_linux_style_file(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            content = FileEndingUtil.windows2linux(content)
        with open(file_path, 'wb') as f:
            f.write(content)

    @staticmethod
    def convert_to_windows_style_file(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
            content = FileEndingUtil.linux2windows(content)
        with open(file_path, 'wb') as f:
            f.write(content)
