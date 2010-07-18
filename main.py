#!/usr/bin/env python
from flask import Flask, render_template
from modules.block_grid import BlockGrid
import modules
import re

app = Flask(__name__)

@app.route('/')
def main_view():
	block_grid = BlockGrid(conf='./layout')
	block_grid.generate()
	return render_template('main_view', block_grid=block_grid)

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')