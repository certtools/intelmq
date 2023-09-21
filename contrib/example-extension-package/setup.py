from pathlib import Path
from setuptools import find_packages, setup


# Instead of the bot-autodiscovery below, you can also just manually declare entrypoints
# (regardless of packaging solution, even in pyproject.toml etc.), e.g.:
#
# intelmq.bots.collectors.custom.collector = mybots.bots.collectors.custom.collector:BOT.run
#
# Important is:
#  - entry point has to start with `intelmq.bots.{type}` (type: collectors, experts, parsers, outputs)
#  - target has to end with `:BOT.run`
#  - entry points have to be in `console_scripts` group


BOTS = []

base_path = Path(__file__).parent / 'mybots/bots'
botfiles = [botfile for botfile in Path(base_path).glob('**/*.py') if botfile.is_file() and not botfile.name.startswith('_')]
for file in botfiles:
    file = Path(str(file).replace(str(base_path), 'intelmq/bots'))
    entry_point = '.'.join(file.with_suffix('').parts)
    file = Path(str(file).replace('intelmq/bots', 'mybots/bots'))
    module = '.'.join(file.with_suffix('').parts)
    BOTS.append('{0} = {1}:BOT.run'.format(entry_point, module))

setup(
    name='intelmq-example-extension',
    version='1.0.0',  # noqa: F821
    maintainer='Your Name',
    maintainer_email='you@example.com',
    packages=find_packages(),
    license='AGPLv3',
    description='This is an example package to demonstrate how ones can extend IntelMQ.',
    entry_points={
        'console_scripts': BOTS
    },
)
