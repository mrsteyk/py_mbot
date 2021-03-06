import logging
from telegram.ext import Updater, CommandHandler
from api import ConfigAPI, LangAPI
import modloader

# TODO: logging by bot
logging.basicConfig(level=logging.INFO)

config = ConfigAPI('main')
tr = LangAPI('main')

updater = Updater(config['token'])
dp = updater.dispatcher


def start(bot, update):
    lang = update.effective_user.language_code
    update.effective_message.reply_text(tr(lang, 'start'))


def help(bot, update, args):
    lang = update.effective_user.language_code
    if len(args) == 0:
        update.effective_message.reply_text(tr(lang, 'help'))
    else:
        module_name = " ".join(args)
        if module_name in modloader.DISABLED or module_name in modloader.FAILURE:
            update.effective_message.reply_text("Module is disabled")
        elif module_name in modloader.ENABLED:
            modloader.ENABLED.get(module_name).help(update.effective_message, [])
        else:
            update.effective_message.reply_text("Module not found")


def about(bot, update):
    lang = update.effective_user.language_code
    update.effective_message.reply_text(tr(lang, 'about').format(config['version']))


def module_list(bot, update):
    lang = update.effective_user.language_code
    modlist = ''
    for module_name in sorted(modloader.ENABLED):
        modlist += ' - {0}\n'.format(module_name)
    fail_modlist = ''
    for (module_name, e) in sorted(modloader.FAILURE.items()):
        fail_modlist += ' - {0}: {1}\n'.format(module_name, e)
    disabled_modlist = ''
    for module_name in sorted(modloader.DISABLED):
        disabled_modlist += ' - {0}\n'.format(module_name)
    update.effective_message.reply_text(tr(lang, 'modules').format(modlist, fail_modlist,
                                                                   disabled_modlist),
                                        parse_mode="HTML")


def main():
    modloader.load_modules(updater)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help, pass_args=True))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(CommandHandler('modules', module_list))
    dp.add_error_handler(lambda bot, update, error: print(error))

    updater.start_polling(clean=True)
    updater.idle()

if __name__ == '__main__':
    main()
