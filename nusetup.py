# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from nudev.api.v3 import ProjectConfigBase, SourceConfigBase


class SourceConfig(SourceConfigBase):
    """Source."""

    name = "aionap"


class ProjectConfig(ProjectConfigBase):
    """Project config."""

    sources = [SourceConfig]

project = ProjectConfig()
