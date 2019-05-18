# coding=utf8
import re


def camel2snake(s):
    camel_to_snake_regex = r'((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))'
    return re.sub(camel_to_snake_regex, r'_\1', s).lower()


def snake2camel(s):
    snake_to_camel_regex = r"(?:^|_)(.)"
    return re.sub(snake_to_camel_regex, lambda m: m.group(1).upper(), s)


def get_percentage_display(value, places=2):
    fmt = '{0:. f}%'.replace(' ', str(places))
    return fmt.format(value * 100)
