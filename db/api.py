import sqlite3
import pandas as pd
import datetime as dt
import pathlib

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath('clips.db').resolve()

