import sys
import types
import unittest
import importlib.util
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


class _FakeSentenceTransformer:
    def __init__(self, *_args, **_kwargs):
        pass


class MessageRepositoryFastSearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_fast_search_aggregates_messages_from_all_chats(self):
        fake_sentence_transformers = types.ModuleType("sentence_transformers")
        fake_sentence_transformers.SentenceTransformer = _FakeSentenceTransformer
        fake_pymongo_errors = types.ModuleType("pymongo.errors")
        fake_pymongo_errors.DuplicateKeyError = type("DuplicateKeyError", (Exception,), {})
        fake_pymongo = types.ModuleType("pymongo")
        fake_pymongo.__path__ = []
        fake_pymongo.errors = fake_pymongo_errors
        fake_core_exceptions = types.ModuleType("core.exceptions")
        fake_core_exceptions.DuplicatedPrimaryKeyError = type("DuplicatedPrimaryKeyError", (Exception,), {})
        fake_core_exceptions.NoContentError = type("NoContentError", (Exception,), {})
        fake_domain_models_mongo = types.ModuleType("domain.models.mongo")
        fake_domain_models_mongo.ContextMessageDao = object
        fake_core_dto = types.ModuleType("core.dto")
        fake_core_dto.MessageDTO = object
        fake_core_mapper = types.ModuleType("core.mapper")
        fake_core_mapper.map_message_dto_to_dao = lambda *_args: None
        fake_repository_abstractions = types.ModuleType("infrastructure.repository.abstractions")
        fake_repository_abstractions.AbstractRepository = object
        modules = {
            "sentence_transformers": fake_sentence_transformers,
            "pymongo": fake_pymongo,
            "pymongo.errors": fake_pymongo_errors,
            "core.exceptions": fake_core_exceptions,
            "domain.models.mongo": fake_domain_models_mongo,
            "core.dto": fake_core_dto,
            "core.mapper": fake_core_mapper,
            "infrastructure.repository.abstractions": fake_repository_abstractions,
        }
        with patch.dict(sys.modules, modules):
            spec = importlib.util.spec_from_file_location(
                "message_repository_under_test",
                "infrastructure/repository/mongo/message_repository.py",
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            MessageRepository = module.MessageRepository

        aggregate = AsyncMock()
        aggregate.return_value.to_list = AsyncMock(return_value=[{"message_id": 42}])
        collection = SimpleNamespace(aggregate=aggregate)
        database = SimpleNamespace(get_collection=lambda _name: collection)
        repository = MessageRepository(SimpleNamespace(get_database=database))

        result = await repository.fast_search(
            SimpleNamespace(chat_id=7, embedding=[0.1, 0.2])
        )

        self.assertEqual(result, 42)
        pipeline = aggregate.await_args.args[0]
        self.assertFalse(any("$match" in stage for stage in pipeline))


if __name__ == "__main__":
    unittest.main()
