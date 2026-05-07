from src.calculator_demo.app import create_root


class FakeRoot:
    def __init__(self) -> None:
        self.title_value = None

    def title(self, value: str) -> None:
        self.title_value = value


class FakeApp:
    def __init__(self, master) -> None:
        self.master = master
        self.grid_called = False
        self.grid_kwargs = None

    def grid(self, **kwargs) -> None:
        self.grid_called = True
        self.grid_kwargs = kwargs


def test_create_root_wires_title_and_app(monkeypatch) -> None:
    fake_root = FakeRoot()
    created = {}

    monkeypatch.setattr('src.calculator_demo.app.tk.Tk', lambda: fake_root)

    def fake_app_factory(master):
        app = FakeApp(master)
        created['app'] = app
        return app

    monkeypatch.setattr('src.calculator_demo.app.CalculatorApp', fake_app_factory)

    root = create_root()

    assert root is fake_root
    assert fake_root.title_value == 'Taschenrechner'
    assert created['app'].master is fake_root
    assert created['app'].grid_called is True
    assert created['app'].grid_kwargs == {'sticky': 'nsew'}
