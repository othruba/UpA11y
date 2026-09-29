from __future__ import annotations

from dataclasses import dataclass, field

from upa11y.orientacoes.orientacao import OrientacaoA11y, RefatoracaoA11y


@dataclass
class EditorSelection:
    current_test_index: int | None = None
    current_refactor_index: int | None = None
    active_tests: set[int] = field(default_factory=set)
    active_refactors: set[tuple[int, int]] = field(default_factory=set)

    def reset(self) -> None:
        self.current_test_index = None
        self.current_refactor_index = None
        self.active_tests.clear()
        self.active_refactors.clear()

    def select_initial(self, orientacoes: tuple[OrientacaoA11y, ...]) -> None:
        self.current_test_index = 0 if orientacoes else None
        self.current_refactor_index = 0 if orientacoes and orientacoes[0].refatoracoes else None
        self.select_all(orientacoes)

    def select_all(self, orientacoes: tuple[OrientacaoA11y, ...]) -> None:
        self.active_tests = set(range(len(orientacoes)))
        self.active_refactors = {
            (test_index, refactor_index)
            for test_index, orientacao in enumerate(orientacoes)
            for refactor_index, _refatoracao in enumerate(orientacao.refatoracoes)
        }

    def trim(self, orientacoes: tuple[OrientacaoA11y, ...]) -> None:
        self.active_tests = {
            index
            for index in self.active_tests
            if 0 <= index < len(orientacoes)
        }
        self.active_refactors = {
            (test_index, refactor_index)
            for test_index, refactor_index in self.active_refactors
            if 0 <= test_index < len(orientacoes)
            and 0 <= refactor_index < len(orientacoes[test_index].refatoracoes)
        }

    def selected_orientacoes(self, orientacoes: tuple[OrientacaoA11y, ...]) -> tuple[OrientacaoA11y, ...]:
        return tuple(
            orientacao
            for index, orientacao in enumerate(orientacoes)
            if index in self.active_tests
        )

    def summary(self, orientacoes: tuple[OrientacaoA11y, ...]) -> str:
        return (
            f"{len(self.active_tests)} de {len(orientacoes)} teste(s) selecionado(s); "
            f"{len(self.active_refactors)} refatoração(ões) selecionada(s)."
        )

    def set_test_checked(self, orientacoes: tuple[OrientacaoA11y, ...], test_index: int, checked: bool) -> None:
        if checked:
            self.active_tests.add(test_index)
            for refactor_index, _refatoracao in enumerate(orientacoes[test_index].refatoracoes):
                self.active_refactors.add((test_index, refactor_index))
            return

        self.active_tests.discard(test_index)
        for refactor_index, _refatoracao in enumerate(orientacoes[test_index].refatoracoes):
            self.active_refactors.discard((test_index, refactor_index))

    def set_refactor_checked(self, test_index: int, refactor_index: int, checked: bool) -> None:
        key = (test_index, refactor_index)
        if checked:
            self.active_tests.add(test_index)
            self.active_refactors.add(key)
        else:
            self.active_refactors.discard(key)

    def current_test(self, orientacoes: tuple[OrientacaoA11y, ...]) -> OrientacaoA11y | None:
        if self.current_test_index is None:
            return None
        if not 0 <= self.current_test_index < len(orientacoes):
            return None
        return orientacoes[self.current_test_index]

    def current_refactor(self, orientacoes: tuple[OrientacaoA11y, ...]) -> RefatoracaoA11y | None:
        orientacao = self.current_test(orientacoes)
        if orientacao is None or self.current_refactor_index is None:
            return None
        if not 0 <= self.current_refactor_index < len(orientacao.refatoracoes):
            return None
        return orientacao.refatoracoes[self.current_refactor_index]
