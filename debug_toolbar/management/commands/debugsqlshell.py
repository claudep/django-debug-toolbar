from __future__ import print_function, unicode_literals

from time import time

from django.db.backends import util

import sqlparse


class PrintQueryWrapper(util.CursorDebugWrapper):
    def execute(self, sql, params=()):
        start_time = time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            raw_sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            end_time = time()
            duration = (end_time - start_time) * 1000
            formatted_sql = sqlparse.format(raw_sql, reindent=True)
            print('%s [%.2fms]' % (formatted_sql, duration))


util.CursorDebugWrapper = PrintQueryWrapper
