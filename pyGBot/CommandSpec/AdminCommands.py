
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

from pyGBot.commands import bot_command
from pyGBot.auth import AuthLevels


log.logger.debug("**** LOADING ADMIN COMMANDS ****")


@bot_command(AuthLevels.Admin)
def ChangeNick(bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify a new nick.')

    args = args.split(' ', 1)
    bot.changenick(args[0])


@bot_command(AuthLevels.Admin)
def Do(bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify a channel to act in.')

    args = args.split(' ', 1)
    if args[0].startswith('#'):
        if args[0] in bot.channels:
            bot.actout(args[0], args[1])
        else:
            bot.noteout(user, 'I am not connected to that channel.')
    else:
        bot.noteout(user, 'Incorrect channel name. Channels must start with #')


@bot_command(AuthLevels.Admin)
def JoinChannel(bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify a channel to join.')

    args = args.split(' ')
    if args[0].startswith('#'):
        if args[0] not in bot.channels:
            log.logger.info(u"Attempting to join channel %s" % args[0])
            if len(args) > 1:
                bot.join(args[0], key=args[1])
            else:
                bot.join(args[0])
        else:
            bot.noteout(user, 'I am already connected to that channel.')
    else:
        bot.noteout(user, 'Incorrect channel name. Channels must start with #')


@bot_command(AuthLevels.Admin)
def Msg(bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify a username to send a message to.')
    else:
        args = args.split(' ',1)
        if len(args) > 1:
            bot.privout(args[0],args[1])
        else:
            bot.noteout(user, 'Please include a message to send.')


@bot_command(AuthLevels.Admin)
def PartChannel(bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify a channel to part.')

    args = args.split(' ')
    if args[0].startswith('#'):
        if args[0] in bot.channels:
            log.logger.info(u'Parting channel %s' % args[0])
            bot.part(args[0])
        else:
            bot.noteout(user, 'I am not in that channel.')
    else:
        bot.noteout(user, 'Incorrect channel name. Channels must start with #')


@bot_command(AuthLevels.Admin)
def Say(bot, channel, user, args):
    args = args.split(' ',1)
    if args == ['']:
        bot.noteout(user, 'Please specify a channel to speak in.')
    elif args[0].startswith('#'):
        if args[0] in bot.channels:
            bot.pubout(args[0],args[1])
        else:
            bot.noteout(user, 'I am not connected to that channel.')
    else:
        bot.noteout(user, 'Incorrect channel name. Channels must start with #')

@bot_command(AuthLevels.Admin)
def UserMode(self, bot, channel, user, args):
    if args == '':
        bot.noteout(user, 'Please specify the mode settings you wish to apply.')

    bot.modestring(bot.nickname, args)



