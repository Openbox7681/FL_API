import logging.config
from app import api
from app.controller.UploadModelController import uploadModel
from app.controller.ExampleController import example
from app.controller.AggModelController import AggModel,QueryGlobalModel




logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)


#模組檔案上傳相關

api.add_resource(uploadModel, '/uploadModel', resource_class_kwargs={
    'logger': logging.getLogger('/uploadModel')
})

#測試API

api.add_resource(example, '/example', resource_class_kwargs={
    'logger': logging.getLogger('/example')
})

#模組聚合API

api.add_resource(AggModel, '/aggModel', resource_class_kwargs={
    'logger': logging.getLogger('/aggModel')
})

api.add_resource(QueryGlobalModel, '/queryGlobalModel', resource_class_kwargs={
    'logger': logging.getLogger('/queryGlobalModel')
})






