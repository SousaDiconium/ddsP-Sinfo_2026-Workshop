import logging
import sys

import pytest
from knowledge_service.utils.logger import InterceptHandler, setup_logger
from pytest_mock import MockerFixture


class TestInterceptHandler:
    def test_emit_with_valid_loguru_level(self, mocker: MockerFixture) -> None:
        # given
        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")
        mock_logger.level.return_value.name = "INFO"
        mock_logger.opt.return_value = mock_logger

        handler = InterceptHandler()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py", lineno=1, msg="Test message", args=(), exc_info=None
        )

        # when
        handler.emit(record)

        # then
        mock_logger.level.assert_called_once_with("INFO")
        mock_logger.opt.assert_called_once_with(depth=1, exception=None)
        mock_logger.log.assert_called_once_with("INFO", "Test message")

    def test_emit_with_invalid_loguru_level(self, mocker: MockerFixture) -> None:
        # given
        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")
        mock_logger.level.side_effect = ValueError("Unknown level")
        mock_logger.opt.return_value = mock_logger

        handler = InterceptHandler()
        record = logging.LogRecord(
            name="test",
            level=99,  # Custom level
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.levelname = "CUSTOM"

        # when
        handler.emit(record)

        # then
        mock_logger.opt.assert_called_once_with(depth=1, exception=None)
        mock_logger.log.assert_called_once_with(99, "Test message")

    def test_emit_finds_correct_caller_depth(self, mocker: MockerFixture) -> None:
        # given
        mock_frame = mocker.patch("inspect.currentframe")
        frame1 = mocker.Mock()
        frame1.f_code.co_filename = logging.__file__  # This should be skipped
        frame1.f_back = None
        frame2 = mocker.Mock()
        frame2.f_code.co_filename = "caller.py"  # This should be found
        frame2.f_back = frame1
        mock_frame.return_value = frame2

        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")
        mock_logger.level.return_value.name = "WARNING"
        mock_logger.opt.return_value = mock_logger

        handler = InterceptHandler()
        record = logging.LogRecord(
            name="test", level=logging.WARNING, pathname="test.py", lineno=1, msg="Test warning", args=(), exc_info=None
        )

        # when
        handler.emit(record)

        # then
        mock_logger.opt.assert_called_once_with(depth=2, exception=None)

    def test_emit_with_exception_info(self, mocker: MockerFixture) -> None:
        # given
        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")
        mock_logger.level.return_value.name = "ERROR"
        mock_logger.opt.return_value = mock_logger

        handler = InterceptHandler()
        exc_info = (Exception, Exception("test error"), None)
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Error message",
            args=(),
            exc_info=exc_info,
        )

        # when
        handler.emit(record)

        # then
        mock_logger.opt.assert_called_once_with(depth=1, exception=exc_info)
        mock_logger.log.assert_called_once_with("ERROR", "Error message")


class TestSetupLogger:
    def test_setup_logger_clears_existing_handlers(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.Mock()
        mock_settings.log_level = logging.INFO

        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")

        # when
        setup_logger(mock_settings)

        # then
        mock_logger.remove.assert_called_once()

    def test_setup_logger_configures_root_logger(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.Mock()
        mock_settings.log_level = logging.DEBUG

        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")
        mock_logging = mocker.patch("knowledge_service.utils.logger.logging")

        # when
        setup_logger(mock_settings)

        # then
        mock_logger.add.assert_called_once()
        args, kwargs = mock_logger.add.call_args

        assert args[0] == sys.stderr
        assert kwargs["format"] == (
            "{time:YYYY-MM-DD HH:mm:ss.SSS}  {level: <5} {process} --- "
            "[{thread.name}] {name}.{function}:{line} : {message}"
        )
        assert kwargs["level"] == logging.DEBUG
        assert kwargs["colorize"] is False

        mock_logging.basicConfig.assert_called_once()
        _, basic_config_kwargs = mock_logging.basicConfig.call_args
        assert basic_config_kwargs["handlers"] == [mocker.ANY]
        assert basic_config_kwargs["level"] == 0
        assert basic_config_kwargs["force"] is True

    @pytest.mark.parametrize(
        "log_level",
        [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ],
    )
    def test_setup_logger_with_different_log_levels(self, log_level: int, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.Mock()
        mock_settings.log_level = log_level

        mock_logger = mocker.patch("knowledge_service.utils.logger.logger")

        # when
        setup_logger(mock_settings)

        # then
        mock_logger.add.assert_called_once()
        _, kwargs = mock_logger.add.call_args
        assert kwargs["level"] == log_level

    def test_setup_logger_patches_uvicorn_loggers(self, mocker: MockerFixture) -> None:
        # given
        mock_settings = mocker.Mock()
        mock_settings.log_level = logging.INFO

        mock_logging = mocker.patch("knowledge_service.utils.logger.logging")

        # when
        setup_logger(mock_settings)

        # then
        for uvicorn_logger_key in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            uvicorn_logger = mock_logging.getLogger(uvicorn_logger_key)
            assert isinstance(uvicorn_logger.handlers[0], InterceptHandler)
            assert uvicorn_logger.propagate is False
