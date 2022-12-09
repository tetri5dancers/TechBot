from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class OnesParams:
    base_url: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    oneSParams: OnesParams


def load_config(path: str = None):
    env = Env()
    env.read_env(path)


    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(),
        oneSParams=OnesParams(env.str('ONES_BASEURL'))
    )

tg_bot_token = '5114732527:AAHnGZxoZXxyjFPwbzjsaEWzhsR4n8HLQ6E'

pyrus_login = 'bot@ef152e07-5aa2-4123-9db6-882f2fa78f79'
pyrus_secret = 'fuZaWmYuHGWMmcwdBKgUegBu3SlydNjEYEjH9P12Q6Tlbm6~jQRyfN~l47pcvMZNPSwqHqVJrnjWzwdOX979N0urgJYO7fqI'