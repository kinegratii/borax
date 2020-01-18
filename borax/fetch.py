# coding=utf8

import warnings

from borax.datasets.fetch import *  # noqa: F403

warnings.warn(
    'This module is deprecated and will be removed in V3.3.Use borax.datasets.fetch instead.',
    category=PendingDeprecationWarning
)
