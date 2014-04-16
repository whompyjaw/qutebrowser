# Copyright 2014 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""CompletionModels for settings/sections."""

from qutebrowser.models.completion import CompletionModel, NoCompletionsError
import qutebrowser.config.configdata as configdata


class SettingSectionCompletionModel(CompletionModel):

    """A CompletionModel filled with settings sections."""

    # pylint: disable=abstract-method

    def __init__(self, parent=None):
        super().__init__(parent)
        cat = self.new_category("Config sections")
        for name in configdata.data.keys():
            self.new_item(cat, name)


class SettingOptionCompletionModel(CompletionModel):

    """A CompletionModel filled with settings and their descriptions."""

    # pylint: disable=abstract-method

    def __init__(self, section, parent=None):
        super().__init__(parent)
        cat = self.new_category("Config options for {}".format(section))
        sectdata = configdata.data[section]
        for name, _ in sectdata.items():
            try:
                desc = sectdata.descriptions[name]
            except (KeyError, AttributeError):
                desc = ""
            self.new_item(cat, name, desc)


class SettingValueCompletionModel(CompletionModel):

    """A CompletionModel filled with setting values."""

    # pylint: disable=abstract-method

    def __init__(self, section, option, parent=None):
        super().__init__(parent)
        cat = self.new_category("Setting values for {}".format(option))
        vals = configdata.data[section][option].typ.valid_values
        if vals is None:
            raise NoCompletionsError
        for val in vals:
            try:
                desc = vals.descriptions[val]
            except KeyError:
                desc = ""
            self.new_item(cat, val, desc)
