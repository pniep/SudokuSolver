from flask import Flask, request
import json
from typing import Tuple
import SudokuSolver

app = Flask(__name__)


@app.route("/")
def route_home():
    base_html = open('templates/base.html', 'r').read()

    content = """<form id="s">{table}<button name="start" value="1">Solve</button></form>"""

    test_data = ((0, 0, 9), (0, 4, 8), (0, 8, 2), (1, 1, 8), (1, 2, 6), (1, 3, 9), (1, 6, 4), (1, 7, 7), (1, 8, 5), (2, 1, 5), (2, 5, 6),
                 (2, 7, 9), (3, 1, 2), (3, 2, 5), (3, 3, 1), (3, 6, 8), (4, 0, 7), (4, 2, 8), (4, 4, 2), (4, 5, 3), (4, 6, 6), (5, 1, 1),
                 (5, 4, 6), (5, 7, 2), (6, 0, 8), (6, 1, 7), (6, 2, 3), (6, 7, 4), (7, 2, 9), (8, 3, 3), (8, 4, 5), (8, 6, 7), (8, 7, 8))

    table = draw_html__sudoku_table(data=test_data, cell_format='<input type="tel" pattern="[0-9]" maxlength="1" name="{cell_y},{cell_x}" value="{cell_value}">')
    content = content.format(table=table)

    output = base_html.format(style=prepare_styles(styles_to_load=['base', 'sudoku_table', 'sudoku_table_form']), content=content, script=prepare_scripts(scripts_to_load=['sudoku_table_form']))

    return output


@app.route("/solve", methods=['POST'])
def route_solve():
    given_data = json.loads(request.form.get('data'))
    solved_data = SudokuSolver.SudokuSolver.solve(given_data)
    base_html = open('templates/base.html', 'r').read()
    if solved_data is False:
        content = '!?!??! *^*&%&$ ??!?!?... sth went wrong'
    else:
        content = draw_html__sudoku_table(data=solved_data, cell_format='<span>{cell_value}</span>')
    output = base_html.format(style=prepare_styles(styles_to_load=['base', 'sudoku_table']), content=content, script='')
    return output


def draw_html__sudoku_table(data: Tuple[Tuple[int, int, int], ...], cell_format: str):
    table_data = {}
    for i in data:
        table_data.setdefault(i[0], {})[i[1]] = i[2]

    table = '<table class="sudoku_table">'
    for by in range(3):
        b_row = '<tr>'
        for bx in range(3):
            b_cell = '<td><table>'
            for sy in range(3):
                s_row = '<tr>'
                for sx in range(3):
                    tcell_y = 3 * by + sy
                    tcell_x = 3 * bx + sx
                    if tcell_y in table_data and tcell_x in table_data[tcell_y]:
                        tcell_value = table_data[tcell_y][tcell_x]
                    else:
                        tcell_value = None
                    s_cell = '<td>{cell_content}</td>'.format(cell_content=cell_format.format(cell_y=tcell_y, cell_x=tcell_x, cell_value='' if tcell_value is None else tcell_value))
                    s_row += s_cell
                s_row += '</tr>'
                b_cell += s_row
            b_cell += '</table></td>'
            b_row += b_cell
        b_row += '</tr>'
        table += b_row
    table += '</table>'
    return table


def prepare_styles(styles_to_load: list):
    styles = """<style type="text/css">{styles}</style>"""
    return styles.format(styles='\n\n'.join([open('styles/' + style_to_load + '.css', 'r').read() for style_to_load in styles_to_load]))


def prepare_scripts(scripts_to_load: list):
    scripts = """<script>{scripts}</script>"""
    return scripts.format(scripts='\n\n'.join([open('scripts/' + script_to_load + '.js', 'r').read() for script_to_load in scripts_to_load]))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
