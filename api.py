import interfaces
import classic_api


def init(database: interfaces.Database) -> None:
    classic_api.init(database)
