from src.config.config import setup_config
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

pytest_plugins = ['src.fixtures.courier', 'src.fixtures.order']


def pytest_configure(config):
    setup_config(config)


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='dev', help='current environment')

