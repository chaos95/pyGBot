##
##    pyGBot - Versatile IRC Bot
##    Copyright (C) 2008 Morgan Lokhorst-Blight, Alex Soborov, Paul Rotering
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

from pyGBot import log

from pyGBot.auth import get_userlevel

commands = {}

aliases = {}


class Command:
    def __init__(self, fn, authlevel):
        self.fn = fn
        self.authlevel = authlevel


#decorator
def bot_command(fn, authlevel):
    command = Command(fn, authlevel)
    commands[fn.__name__] = command
    return fn


def add_alias(friendlyname, commandname):
    if not commandname in commands:
        log.logger.warn(
            'Unable to add alias %s for command %s - command not found' %
            (friendlyname, commandname))

    aliases[friendlyname] = commandname


# MESSAGE PROCESSING
def process_message(bot, channel, user, message):
    elems = message.split(' ', 1)
    commandname = elems[0]
    origcommandname = commandname
    if len(elems) > 1:
        arg = elems[1]
    else:
        arg = ""

    # Translate the alias to the base command name
    if commandname in aliases:
        commandname = aliases[commandname]

    if commandname not in commands:
        bot.noteout(user, 'Command not recognised: %s' % origcommandname)
        return

    command = commands[commandname]

    userlevel = get_userlevel(user)

    if userlevel < command.level:
        errormsg = 'Insufficient access level for command: %s ' \
            'Required level: %s Your level: %s' % \
            (origcommandname, str(command.level), str(userlevel))
        bot.noteout(user, errormsg)
        return

    command(bot, channel, user, arg)
