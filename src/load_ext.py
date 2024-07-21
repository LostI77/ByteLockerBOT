#import importlib
#import os

#async def load_extensions(bot, pathCommands):
#    for path in pathCommands:
#        for root, _, files in os.walk(path):
#            for file in files:
#                if file.endswith(".py"):
#                    ext_path = os.path.join(root, file).replace(os.sep, ".")[:-3]
#                    try:
#                        await bot.load_extension(ext_path)
#                        print(f"Cargada la extensión {ext_path}")
#                    except Exception as e:
#                        print(f"No se pudo cargar la extensión {ext_path}. Error: {e}")

async def load_extensions(bot, extensions):
    for ext in extensions:
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(f'No se pudo cargar la extensión {ext}. Error: {e}')