from os import listdir
import api

ENABLED = {}
DISABLED = []
FAILURE = {}


def load_modules(updater):
    telegram_api = api.TelegramAPI(updater)

    for module_name in listdir('./modules'):
        if not module_name.startswith('lib-') and module_name.endswith('.py'):
            module_name = module_name[:-3]
        try:
            current_module = getattr(__import__('modules.{0}'.format(module_name)), module_name)
            loaded_module = current_module.TelegramModule(telegram_api)
        except Exception as e:
            FAILURE.update({module_name: e})
            continue

        if loaded_module.friendly_name:
            module_name = loaded_module.friendly_name

        if module_name in ENABLED or module_name in DISABLED:
            FAILURE.update({module_name: 'Module {0} is already loaded!'.format(module_name)})

        if loaded_module.disabled:
            DISABLED.append(module_name)
            continue

        ENABLED.update({module_name: loaded_module})
