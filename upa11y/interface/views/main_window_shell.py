from __future__ import annotations

from pathlib import Path
from typing import Any

from PyQt6.Qsci import QsciLexerPython, QsciScintilla
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
import qtawesome as qta

from upa11y.analise.processador import ResultadoAnalise, analisar_caminho
from upa11y.interface.views.editor_state import EditorSelection
from upa11y.interface.widgets.sidebar_tree import SidebarTreeWidget
from upa11y.interface.widgets.top_bar import TopBar
from upa11y.orientacoes import CONJUNTO_VAZIO
from upa11y.orientacoes.orientacao import ConjuntoOrientacoes, OrientacaoA11y, RefatoracaoA11y
from upa11y.orientacoes.serializacao import conjunto_de_dict, conjunto_para_dict, exportar_conjunto, importar_conjunto


class MainWindowShell(QWidget):
    home_requested = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("mainShellRoot")
        self.conjunto: ConjuntoOrientacoes = CONJUNTO_VAZIO
        self.orientacoes = self.conjunto.orientacoes
        self.last_result: ResultadoAnalise | None = None
        self.selection = EditorSelection()
        self.updating_tree_checks = False
        self._stack_pages: dict[str, int] = {}
        self._build_ui()
        self._connect_events()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self.top_bar = TopBar(self)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        self.sidebar = SidebarTreeWidget(self)
        self.sidebar.setMinimumWidth(320)
        self.sidebar.setMaximumWidth(480)
        self.sidebar.set_data(self._orientation_tree())

        self.content_stack = QStackedWidget(self)
        self.content_stack.setObjectName("contentStack")

        self._add_page("utils", self._create_utils_page())
        self._add_page("testes", self._create_tests_page())
        self._add_page("refatoracoes", self._create_refactor_page())
        self._add_page("processar", self._create_process_page())
        self._add_page("resultados", self._create_results_page())

        content_layout.addWidget(self.sidebar, 3)
        content_layout.addWidget(self.content_stack, 7)

        layout.addWidget(self.top_bar)
        layout.addLayout(content_layout)

        self._render_editor()
        self.show_page("utils")

    def _connect_events(self) -> None:
        self.top_bar.home_click.connect(self.home_requested.emit)
        self.top_bar.utils_click.connect(lambda: self.show_page("utils"))
        self.top_bar.testes_click.connect(lambda: self.show_page("testes"))
        self.top_bar.refatoracoes_click.connect(lambda: self.show_page("refatoracoes"))
        self.top_bar.processar_click.connect(lambda: self.show_page("processar"))
        self.top_bar.resultados_click.connect(lambda: self.show_page("resultados"))
        self.sidebar.tree.currentItemChanged.connect(self._on_tree_selection_changed)
        self.sidebar.tree.itemChanged.connect(self._on_tree_item_changed)

    def _add_page(self, key: str, page: QWidget) -> None:
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("contentScroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(page)

        index = self.content_stack.addWidget(scroll_area)
        self._stack_pages[key] = index

    def show_page(self, key: str) -> None:
        self.content_stack.setCurrentIndex(self._stack_pages[key])
        self.top_bar.set_active(key)

    def _create_utils_page(self) -> QWidget:
        page, layout = self._create_workspace_page()
        layout.addWidget(self._page_title("Utils e conjunto"))
        layout.addWidget(
            self._description(
                "Importe o JSON, ajuste o título do conjunto e edite as funções compartilhadas pelos testes."
            )
        )

        layout.addLayout(self._editor_actions())

        self.orientacoes_status = self._status_label()
        layout.addWidget(self.orientacoes_status)

        self.conjunto_titulo_input = self._form_input("")
        layout.addWidget(self._field_label("Título"))
        layout.addWidget(self.conjunto_titulo_input)

        layout.addWidget(self._field_label("Utils compartilhados"))
        self.utils_editor = self._python_editor("", minimum_height=640)
        layout.addWidget(self.utils_editor)
        return page

    def _create_tests_page(self) -> QWidget:
        page, layout = self._create_workspace_page()
        layout.addWidget(self._page_title("Teste selecionado"))
        layout.addWidget(
            self._description(
                "Selecione um teste na árvore lateral para visualizar e editar o código de verificação."
            )
        )
        layout.addLayout(self._editor_actions())

        self.testes_status = self._status_label()
        layout.addWidget(self.testes_status)

        self.test_id_input = self._form_input("")
        self.test_description_input = self._form_input("")
        self.test_function_input = self._form_input("testar")

        fields = QHBoxLayout()
        fields.setSpacing(10)
        fields.addLayout(self._field_group("Identificador", self.test_id_input), 1)
        fields.addLayout(self._field_group("Descrição", self.test_description_input), 3)
        fields.addLayout(self._field_group("Função do teste", self.test_function_input), 1)
        layout.addLayout(fields)

        layout.addWidget(self._field_label("Código do teste"))
        self.test_code_editor = self._python_editor("", minimum_height=680)
        layout.addWidget(self.test_code_editor)
        return page

    def _create_refactor_page(self) -> QWidget:
        page, layout = self._create_workspace_page()
        layout.addWidget(self._page_title("Refatoração selecionada"))
        layout.addWidget(
            self._description(
                "Selecione uma refatoração na árvore lateral ou adicione uma nova ao teste ativo."
            )
        )
        layout.addLayout(self._editor_actions(include_add_refactor=True))

        self.refatoracoes_status = self._status_label()
        layout.addWidget(self.refatoracoes_status)

        self.refactor_selection_label = QLabel("Nenhuma refatoração selecionada.")
        self.refactor_selection_label.setObjectName("statusLabel")
        self.refactor_selection_label.setWordWrap(True)
        layout.addWidget(self.refactor_selection_label)
        self.refactor_title_input = self._form_input("")
        self.refactor_description_input = self._form_input("")
        self.refactor_function_input = self._form_input("refatorar")

        fields = QHBoxLayout()
        fields.setSpacing(10)
        fields.addLayout(self._field_group("Título", self.refactor_title_input), 1)
        fields.addLayout(self._field_group("Descrição", self.refactor_description_input), 3)
        fields.addLayout(self._field_group("Função da refatoração", self.refactor_function_input), 1)
        layout.addLayout(fields)

        layout.addWidget(self._field_label("Código da refatoração"))
        self.refactor_code_editor = self._python_editor("", minimum_height=680)
        layout.addWidget(self.refactor_code_editor)
        return page

    def _editor_actions(self, *, include_add_refactor: bool = False) -> QHBoxLayout:
        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addWidget(self._inline_button("Importar JSON", "fa5s.file-import", self._import_orientacoes))
        actions.addWidget(self._inline_button("Salvar edição", "fa5s.save", self._save_editor_changes))
        if include_add_refactor:
            actions.addWidget(self._inline_button("Adicionar refatoração", "fa5s.plus", self._add_refactor))
        actions.addWidget(self._inline_button("Exportar JSON", "fa5s.file-export", self._export_orientacoes))
        actions.addWidget(self._inline_button("Limpar conjunto", "fa5s.undo", self._clear_orientacoes))
        actions.addStretch(1)
        return actions

    def _create_process_page(self) -> QWidget:
        page, layout = self._create_workspace_page()
        layout.addWidget(self._page_title("Processar arquivos"))
        layout.addWidget(self._description("Escolha uma pasta ou arquivo HTML. Pastas são analisadas recursivamente."))

        layout.addWidget(self._field_label("Arquivo ou pasta alvo"))
        path_row = QHBoxLayout()
        path_row.setSpacing(10)

        self.path_input = self._form_input("")
        self.path_input.setPlaceholderText("Digite sample ou escolha uma pasta/arquivo HTML")
        path_row.addWidget(self.path_input, 1)
        path_row.addWidget(self._inline_button("Pasta", "fa5s.folder-open", self._select_folder))
        path_row.addWidget(self._inline_button("Arquivo", "fa5s.file-code", self._select_file))
        layout.addLayout(path_row)

        self.process_status = QLabel("Nenhuma análise executada nesta sessão.")
        self.process_status.setObjectName("statusLabel")
        self.process_status.setWordWrap(True)
        layout.addWidget(self.process_status)

        self.run_button = self._create_action_tile(
            "Executar testes de acessibilidade",
            "fa5s.play",
            self._run_analysis,
        )
        self.run_button.setMaximumWidth(380)
        layout.addWidget(self.run_button)
        layout.addStretch(1)
        return page

    def _create_results_page(self) -> QWidget:
        page, layout = self._create_workspace_page()
        layout.addWidget(self._page_title("Resultados"))

        self.results_summary = QLabel()
        self.results_summary.setObjectName("statusLabel")
        self.results_summary.setWordWrap(True)
        layout.addWidget(self.results_summary)

        self.results_table = QTableWidget(0, 6, self)
        self.results_table.setObjectName("resultsTable")
        self.results_table.setHorizontalHeaderLabels(
            ["Arquivo", "Rec", "Severidade", "Elemento", "Problema", "Sugestão"]
        )
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.setWordWrap(True)
        self.results_table.setMinimumHeight(480)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.results_table)

        self._render_results()
        return page

    def _select_folder(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Selecionar pasta", self.path_input.text() or str(Path.cwd()))
        if selected:
            self.path_input.setText(selected)

    def _select_file(self) -> None:
        selected, _filter = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo HTML",
            self.path_input.text() or str(Path.cwd()),
            "Arquivos HTML (*.html *.htm)",
        )
        if selected:
            self.path_input.setText(selected)

    def _run_analysis(self) -> None:
        caminho = self.path_input.text().strip()
        if not caminho:
            self.process_status.setText("Informe uma pasta ou arquivo HTML antes de executar.")
            return
        if not self.orientacoes:
            self.process_status.setText("Importe um arquivo JSON de orientações antes de executar.")
            self.show_page("utils")
            return

        saved = self._save_editor_changes(silent=True)
        if not saved:
            self.process_status.setText("Corrija o código do editor antes de executar a análise.")
            self.show_page("testes")
            return

        selected_orientacoes = self._selected_orientacoes()
        if not selected_orientacoes:
            self.process_status.setText("Selecione pelo menos um teste na árvore lateral.")
            return

        self.run_button.setEnabled(False)
        self.process_status.setText("Executando testes de acessibilidade...")
        try:
            self.last_result = analisar_caminho(caminho, selected_orientacoes)
            self.path_input.setText(str(self.last_result.origem))
            self._render_results()
            self._update_process_status(self.last_result)
            self.show_page("resultados")
        finally:
            self.run_button.setEnabled(True)

    def _update_process_status(self, resultado: ResultadoAnalise) -> None:
        if resultado.erros:
            self.process_status.setText(" ".join(resultado.erros))
            return

        contagem = resultado.contagem_severidade
        self.process_status.setText(
            f"Análise concluída: {resultado.arquivos_processados} arquivo(s), "
            f"{resultado.total_achados} achado(s), "
            f"{contagem.get('error', 0)} erro(s), "
            f"{contagem.get('warning', 0)} aviso(s)."
        )

    def _render_results(self) -> None:
        self.results_table.setRowCount(0)

        if self.last_result is None:
            self.results_summary.setText("Nenhuma análise executada. Use a aba Processar.")
            return

        resultado = self.last_result
        if resultado.erros:
            self.results_summary.setText("Não foi possível executar a análise.")
            for erro in resultado.erros:
                self._add_result_row(
                    str(resultado.origem),
                    "",
                    "Erro",
                    "entrada",
                    erro,
                    "Selecione uma pasta ou arquivo HTML válido.",
                )
            return

        contagem = resultado.contagem_severidade
        self.results_summary.setText(
            f"{resultado.arquivos_processados} arquivo(s) analisado(s), "
            f"{resultado.total_achados} achado(s), "
            f"{contagem.get('error', 0)} erro(s), "
            f"{contagem.get('warning', 0)} aviso(s)."
        )

        for arquivo in resultado.arquivos:
            nome_arquivo = arquivo.caminho_relativo(resultado.origem)
            if arquivo.erro:
                self._add_result_row(nome_arquivo, "", "Erro", "arquivo", arquivo.erro, "Verifique se o arquivo pode ser lido.")
                continue

            if not arquivo.achados:
                self._add_result_row(nome_arquivo, "", "OK", "document", "Nenhum problema detectado pelas orientações atuais.", "")
                continue

            for achado in arquivo.achados:
                self._add_result_row(
                    nome_arquivo,
                    achado.recomendacao,
                    self._severity_label(achado.severidade),
                    achado.elemento,
                    achado.problema,
                    achado.sugestao,
                )

        self.results_table.resizeRowsToContents()

    def _import_orientacoes(self) -> None:
        selected, _filter = QFileDialog.getOpenFileName(
            self,
            "Importar orientações",
            str(Path.cwd()),
            "Orientações UpA11y (*.json)",
        )
        if not selected:
            return False

        try:
            self._load_conjunto(importar_conjunto(selected), f"Orientações importadas de {selected}.")
            self.show_page("utils")
            return True
        except Exception as erro:  # noqa: BLE001 - feedback direto para o usuario.
            self._set_status(f"Não foi possível importar orientações: {erro}")
            return False

    def _new_conjunto(self) -> None:
        conjunto = ConjuntoOrientacoes(titulo="Novo conjunto")
        self._load_conjunto(conjunto, "Novo conjunto criado.")
        self.show_page("utils")

    def _export_orientacoes(self) -> None:
        if not self._save_editor_changes(silent=True):
            return

        selected, _filter = QFileDialog.getSaveFileName(
            self,
            "Exportar orientações",
            str(Path.cwd() / "orientacoes-upa11y.json"),
            "Orientações UpA11y (*.json)",
        )
        if not selected:
            return

        destino = exportar_conjunto(self.conjunto, selected)
        self._set_status(f"Orientações exportadas para {destino}.")

    def _clear_orientacoes(self) -> None:
        self.selection.reset()
        self._load_conjunto(CONJUNTO_VAZIO, "Nenhum conjunto de orientações está carregado.")

    def _load_conjunto(self, conjunto: ConjuntoOrientacoes, mensagem: str) -> None:
        self.conjunto = conjunto
        self.orientacoes = self.conjunto.orientacoes
        self.selection.select_initial(self.orientacoes)
        self.last_result = None
        self._refresh_all_views(mensagem)

    def _refresh_all_views(self, mensagem: str) -> None:
        self._refresh_sidebar()
        self._render_editor()
        self._render_results()
        self._set_status(mensagem)

    def _render_editor(self) -> None:
        self.conjunto_titulo_input.setText(self.conjunto.titulo)
        self.utils_editor.setText(self.conjunto.codigo_utils)

        orientacao = self._current_test()
        self._set_test_fields_enabled(orientacao is not None)
        if orientacao is None:
            self.test_id_input.setText("")
            self.test_description_input.setText("")
            self.test_function_input.setText("testar")
            self.test_code_editor.setText("")
            self._render_refactor_editor(None)
            self._set_status("Importe um JSON para visualizar e editar testes.")
            return

        self.test_id_input.setText(orientacao.num_orientacao)
        self.test_description_input.setText(orientacao.descricao)
        self.test_function_input.setText(orientacao.funcao_teste)
        self.test_code_editor.setText(orientacao.codigo_teste)
        self._render_refactor_editor(self._current_refactor())
        self._set_status(
            f"{len(self.orientacoes)} teste(s) carregado(s). "
            f"{len(orientacao.refatoracoes)} refatoração(ões) no teste selecionado. "
            f"{self._selection_summary()}"
        )

    def _render_refactor_editor(self, refatoracao: RefatoracaoA11y | None) -> None:
        enabled = refatoracao is not None
        self._set_refactor_fields_enabled(enabled)
        if refatoracao is None:
            self.refactor_selection_label.setText("Nenhuma refatoração selecionada.")
            self.refactor_title_input.setText("")
            self.refactor_description_input.setText("")
            self.refactor_function_input.setText("refatorar")
            self.refactor_code_editor.setText("")
            return

        self.refactor_selection_label.setText(f"Refatoração: {refatoracao.titulo}")
        self.refactor_title_input.setText(refatoracao.titulo)
        self.refactor_description_input.setText(refatoracao.descricao)
        self.refactor_function_input.setText(refatoracao.funcao_refatoracao)
        self.refactor_code_editor.setText(refatoracao.codigo_refatoracao)

    def _save_editor_changes(self, silent: bool = False) -> bool:
        try:
            data = self._edited_conjunto_data()
            new_conjunto = conjunto_de_dict(data, origem=Path("<editor>"))
        except Exception as erro:  # noqa: BLE001 - feedback direto para o usuario.
            if not silent:
                self._set_status(f"Não foi possível salvar a edição: {erro}")
            return False

        self.conjunto = new_conjunto
        self.orientacoes = self.conjunto.orientacoes
        self._trim_selection()
        self._refresh_sidebar()
        if not silent:
            self._set_status("Edição salva e código recompilado.")
        return True

    def _edited_conjunto_data(self) -> dict[str, Any]:
        data = conjunto_para_dict(self.conjunto)
        data["titulo"] = self.conjunto_titulo_input.text().strip() or "Conjunto sem título"
        data["utils"] = self.utils_editor.text()

        if self.selection.current_test_index is None:
            return data

        test_data = data["orientacoes"][self.selection.current_test_index]
        test_data["num_orientacao"] = self.test_id_input.text().strip()
        test_data["descricao"] = self.test_description_input.text().strip()
        test_data["funcao"] = self.test_function_input.text().strip() or "testar"
        test_data["codigo"] = self.test_code_editor.text()

        if self.selection.current_refactor_index is not None:
            refactor_data = test_data.setdefault("refatoracoes", [])[self.selection.current_refactor_index]
            refactor_data["titulo"] = self.refactor_title_input.text().strip()
            refactor_data["descricao"] = self.refactor_description_input.text().strip()
            refactor_data["funcao"] = self.refactor_function_input.text().strip() or "refatorar"
            refactor_data["codigo"] = self.refactor_code_editor.text()

        return data

    def _add_refactor(self) -> None:
        if self.selection.current_test_index is None:
            self._set_status("Selecione um teste antes de adicionar uma refatoração.")
            return

        if not self._save_editor_changes(silent=True):
            self._set_status("Salve ou corrija o teste antes de adicionar uma refatoração.")
            return

        data = conjunto_para_dict(self.conjunto)
        test_data = data["orientacoes"][self.selection.current_test_index]
        refatoracoes = test_data.setdefault("refatoracoes", [])
        refatoracoes.append(
            {
                "titulo": f"Refatoração {len(refatoracoes) + 1}",
                "descricao": "Refatoração associada a este teste.",
                "funcao": "refatorar",
                "codigo": "def refatorar(documento, achado=None):\n    return documento\n",
            }
        )

        self.conjunto = conjunto_de_dict(data, origem=Path("<editor>"))
        self.orientacoes = self.conjunto.orientacoes
        self.selection.current_refactor_index = len(refatoracoes) - 1
        self.selection.set_refactor_checked(
            self.selection.current_test_index,
            self.selection.current_refactor_index,
            True,
        )
        self._refresh_all_views("Refatoração adicionada ao teste selecionado.")

    def _on_tree_selection_changed(self, current, _previous) -> None:
        if current is None:
            return

        path = self._item_path(current)
        test_index = self._extract_tree_index(path, level=0)
        refactor_index = None
        if "refatoracoes" in path:
            refactor_index = self._extract_tree_index(path, level=len(path) - 1)

        if test_index is not None and 0 <= test_index < len(self.orientacoes):
            self.selection.current_test_index = test_index
            orientacao = self.orientacoes[test_index]
            if refactor_index is not None and 0 <= refactor_index < len(orientacao.refatoracoes):
                self.selection.current_refactor_index = refactor_index
            else:
                self.selection.current_refactor_index = 0 if orientacao.refatoracoes else None
            self.show_page("refatoracoes" if "refatoracoes" in path else "testes")
            self._render_editor()

    def _on_tree_item_changed(self, item, _column) -> None:
        if self.updating_tree_checks:
            return

        path = self._item_path(item)
        test_index = self._extract_tree_index(path, level=0)
        if test_index is None or not 0 <= test_index < len(self.orientacoes):
            return

        checked = item.checkState(0) == Qt.CheckState.Checked
        refactor_index = None
        if "refatoracoes" in path:
            refactor_index = self._extract_tree_index(path, level=len(path) - 1)

        if refactor_index is None:
            self._set_test_checked(test_index, checked)
        elif 0 <= refactor_index < len(self.orientacoes[test_index].refatoracoes):
            self._set_refactor_checked(test_index, refactor_index, checked)

        self._apply_tree_checks()
        self._set_status(self._selection_summary())

    def _add_result_row(
        self,
        arquivo: str,
        recomendacao: str,
        severidade: str,
        elemento: str,
        problema: str,
        sugestao: str,
    ) -> None:
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        for column, value in enumerate((arquivo, recomendacao, severidade, elemento, problema, sugestao)):
            item = QTableWidgetItem(value)
            item.setToolTip(value)
            self.results_table.setItem(row, column, item)

    def _refresh_sidebar(self) -> None:
        self.updating_tree_checks = True
        self.sidebar.set_data(self._orientation_tree())
        self._apply_tree_checks()
        self.updating_tree_checks = False

    def _select_all_items(self) -> None:
        self.selection.select_all(self.orientacoes)

    def _trim_selection(self) -> None:
        self.selection.trim(self.orientacoes)

    def _selected_orientacoes(self) -> tuple[OrientacaoA11y, ...]:
        return self.selection.selected_orientacoes(self.orientacoes)

    def _selection_summary(self) -> str:
        return self.selection.summary(self.orientacoes)

    def _set_test_checked(self, test_index: int, checked: bool) -> None:
        self.selection.set_test_checked(self.orientacoes, test_index, checked)

    def _set_refactor_checked(self, test_index: int, refactor_index: int, checked: bool) -> None:
        self.selection.set_refactor_checked(test_index, refactor_index, checked)

    def _apply_tree_checks(self) -> None:
        self.updating_tree_checks = True
        try:
            for test_index in range(self.sidebar.tree.topLevelItemCount()):
                test_item = self.sidebar.tree.topLevelItem(test_index)
                self._set_item_checked(test_item, test_index in self.selection.active_tests)
                self._apply_refactor_checks(test_item, test_index)
        finally:
            self.updating_tree_checks = False

    def _apply_refactor_checks(self, test_item, test_index: int) -> None:
        for child_index in range(test_item.childCount()):
            child = test_item.child(child_index)
            if child.text(0) != "refatoracoes":
                continue

            for refactor_index in range(child.childCount()):
                refactor_item = child.child(refactor_index)
                checked = (test_index, refactor_index) in self.selection.active_refactors
                self._set_item_checked(refactor_item, checked)

    @staticmethod
    def _set_item_checked(item, checked: bool) -> None:
        if item.flags() & Qt.ItemFlag.ItemIsUserCheckable:
            state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
            item.setCheckState(0, state)

    def _orientation_tree(self) -> dict[str, dict[str, Any]]:
        if not self.orientacoes:
            return {self.conjunto.titulo: {"Nenhuma orientação importada": None}}

        return {
            self.conjunto.titulo: {
                self._test_tree_label(index, orientacao): {
                    "teste.py": None,
                    "refatoracoes": self._refactor_tree(orientacao),
                }
                for index, orientacao in enumerate(self.orientacoes)
            }
        }

    def _refactor_tree(self, orientacao: OrientacaoA11y) -> dict[str, None]:
        if not orientacao.refatoracoes:
            return {"sem refatorações": None}
        return {
            f"{index + 1:02d}. {refatoracao.titulo}": None
            for index, refatoracao in enumerate(orientacao.refatoracoes)
        }

    @staticmethod
    def _test_tree_label(index: int, orientacao: OrientacaoA11y) -> str:
        return f"{index + 1:02d}. {orientacao.num_orientacao} - {orientacao.descricao}"

    def _current_test(self) -> OrientacaoA11y | None:
        return self.selection.current_test(self.orientacoes)

    def _current_refactor(self) -> RefatoracaoA11y | None:
        return self.selection.current_refactor(self.orientacoes)

    @staticmethod
    def _item_path(item) -> tuple[str, ...]:
        labels: list[str] = []
        current = item
        while current is not None:
            labels.append(current.text(0))
            current = current.parent()
        return tuple(reversed(labels))

    @staticmethod
    def _extract_tree_index(path: tuple[str, ...], *, level: int) -> int | None:
        if level < 0 or level >= len(path):
            return None
        number = path[level].split(".", 1)[0]
        return int(number) - 1 if number.isdigit() else None

    def _create_workspace_page(self) -> tuple[QWidget, QVBoxLayout]:
        page = QWidget(self)
        page.setObjectName("workspacePage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return page, layout

    def _create_action_tile(self, text: str, icon_name: str, callback) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("actionTile")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(92)
        button.setIcon(qta.icon(icon_name, color="#f3f5f4"))
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(callback)
        return button

    def _inline_button(self, text: str, icon_name: str, callback) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("inlineButton")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(44)
        button.setIcon(qta.icon(icon_name, color="#f3f5f4"))
        button.setIconSize(QSize(16, 16))
        button.clicked.connect(callback)
        return button

    def _status_label(self, text: str = "") -> QLabel:
        label = QLabel(text)
        label.setObjectName("statusLabel")
        label.setWordWrap(True)
        return label

    def _field_group(self, label_text: str, input_field: QLineEdit) -> QVBoxLayout:
        group = QVBoxLayout()
        group.setSpacing(6)
        group.addWidget(self._field_label(label_text))
        group.addWidget(input_field)
        return group

    def _set_status(self, text: str) -> None:
        for name in ("orientacoes_status", "testes_status", "refatoracoes_status"):
            label = getattr(self, name, None)
            if label is not None:
                label.setText(text)

    def _python_editor(self, code: str, *, minimum_height: int) -> QsciScintilla:
        editor = QsciScintilla(self)
        editor.setText(code)
        editor.setMinimumHeight(minimum_height)
        editor.setTabWidth(4)
        editor.setIndentationsUseTabs(False)
        editor.setAutoIndent(True)
        editor.setMarginLineNumbers(0, True)
        editor.setMarginWidth(0, "0000")
        editor.setCaretLineVisible(True)
        editor.setPaper(QColor("#2f3437"))
        editor.setColor(QColor("#f3f5f4"))
        editor.setMarginsBackgroundColor(QColor("#25292c"))
        editor.setMarginsForegroundColor(QColor("#c6d0cc"))
        editor.setCaretForegroundColor(QColor("#ffffff"))
        editor.setCaretLineBackgroundColor(QColor("#394044"))
        editor.setSelectionBackgroundColor(QColor("#115c22"))

        font = QFont("Noto Sans Mono", 11)
        editor.setFont(font)
        lexer = QsciLexerPython(editor)
        lexer.setDefaultFont(font)
        lexer.setDefaultPaper(QColor("#2f3437"))
        lexer.setDefaultColor(QColor("#f3f5f4"))

        for style in range(128):
            lexer.setPaper(QColor("#2f3437"), style)
            lexer.setFont(font, style)

        lexer.setColor(QColor("#8fd694"), QsciLexerPython.Comment)
        lexer.setColor(QColor("#ffd166"), QsciLexerPython.Keyword)
        lexer.setColor(QColor("#f4a261"), QsciLexerPython.Number)
        lexer.setColor(QColor("#9be7ff"), QsciLexerPython.DoubleQuotedString)
        lexer.setColor(QColor("#9be7ff"), QsciLexerPython.SingleQuotedString)
        lexer.setColor(QColor("#9be7ff"), QsciLexerPython.TripleDoubleQuotedString)
        lexer.setColor(QColor("#9be7ff"), QsciLexerPython.TripleSingleQuotedString)
        lexer.setColor(QColor("#a7c7ff"), QsciLexerPython.FunctionMethodName)
        lexer.setColor(QColor("#c5a3ff"), QsciLexerPython.ClassName)
        lexer.setColor(QColor("#ffffff"), QsciLexerPython.Operator)
        lexer.setColor(QColor("#f3f5f4"), QsciLexerPython.Identifier)
        lexer.setColor(QColor("#ff9ab3"), QsciLexerPython.Decorator)
        editor.setLexer(lexer)
        return editor

    @staticmethod
    def _form_input(value: str) -> QLineEdit:
        input_field = QLineEdit(value)
        input_field.setObjectName("formInput")
        input_field.setMinimumHeight(44)
        return input_field

    @staticmethod
    def _severity_label(severidade: str) -> str:
        labels = {
            "error": "Erro",
            "warning": "Aviso",
            "info": "Info",
        }
        return labels.get(severidade.lower(), severidade)

    @staticmethod
    def _page_title(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("contentTitle")
        label.setWordWrap(True)
        return label

    @staticmethod
    def _section_title(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    @staticmethod
    def _description(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("contentDescription")
        label.setWordWrap(True)
        return label

    @staticmethod
    def _field_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("fieldLabel")
        return label

    def _set_test_fields_enabled(self, enabled: bool) -> None:
        for widget in (
            self.test_id_input,
            self.test_description_input,
            self.test_function_input,
            self.test_code_editor,
        ):
            widget.setEnabled(enabled)

    def _set_refactor_fields_enabled(self, enabled: bool) -> None:
        for widget in (
            self.refactor_title_input,
            self.refactor_description_input,
            self.refactor_function_input,
            self.refactor_code_editor,
        ):
            widget.setEnabled(enabled)
