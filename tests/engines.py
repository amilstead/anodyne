import mock
import unittest

from anodyne import engines


class EnginesTest(unittest.TestCase):

    def test_setup_engine_with_url(self):
        backend_name = "setup_engine_with_url"
        url_key = "_".join(["anodyne", backend_name, "url"]).upper()
        env_dict = {
            "ANODYNE_BACKENDS": backend_name,
            url_key: "sqlite:///tmp/%s.sqlite" % backend_name
        }
        with mock.patch.dict("os.environ", env_dict):
            engines.setup_engine(backend_name)

        engine_data = engines.engines[backend_name]
        # do asserts.
        self.assertIsNotNone(engine_data)
        engine = engine_data["engine"]
        self.assertEqual("sqlite", engine.url.drivername)

    def test_setup_engine_with_envvars(self):
        backend_name = "setup_engine_with_envvars"
        env_vars = {
            "driver": "mysql",
            "host": "localhost",
            "port": "3306",
            "user": "foo",
            "pass": "bar",
            "name": "baz"
        }
        env_dict = {
            "ANODYNE_BACKENDS": backend_name,
        }
        for key, val in env_vars.items():
            env_key = "_".join(["anodyne", backend_name, key]).upper()
            env_dict[env_key] = val
        with mock.patch.dict("os.environ", env_dict):
            engines.setup_engine(backend_name)

        engine_data = engines.engines[backend_name]
        # do asserts.
        self.assertIsNotNone(engine_data)
        engine = engine_data["engine"]
        self.assertEqual("mysql", engine.url.drivername)

    def test_scan(self):
        backend0 = "scan0"
        backend1 = "scan1"
        url_key0 = "_".join(["anodyne", backend0, "url"]).upper()
        url_key1 = "_".join(["anodyne", backend1, "url"]).upper()
        env_dict = {
            "ANODYNE_BACKENDS": ",".join([backend0, backend1]),
            url_key0: "sqlite:///tmp/%s.sqlite" % backend0,
            url_key1: "sqlite:///tmp/%s.sqlite" % backend1
        }
        with mock.patch.dict("os.environ", env_dict):
            engines.scan()

        engine_data0 = engines.engines[backend0]
        # do asserts.
        self.assertIsNotNone(engine_data0)
        engine = engine_data0["engine"]
        self.assertEqual("sqlite", engine.url.drivername)

        engine_data1 = engines.engines[backend1]
        # do asserts.
        self.assertIsNotNone(engine_data1)
        engine = engine_data1["engine"]
        self.assertEqual("sqlite", engine.url.drivername)

    def test_register_failure_callback(self):
        pass

    def test_poke_engine(self):
        pass

    def test_mark_failed(self):
        pass

    def test_get_engine(self):
        pass

    def test_clean_engines(self):
        pass
