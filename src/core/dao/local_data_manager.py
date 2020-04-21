# coding: utf-8
import win32com.client
from ui.console import terminal


class LocalDataManager(object):
    def __init__(self, app_session):
        self.__app_session = app_session
        self.__database = self.__app_session.cfg.database
        self.__local_storage = self.__app_session.cfg.local_storage
        self.__server_storage = self.__app_session.cfg.server_storage

    def get_submodels_list_from_database(self, cml_bench_path):
        return self.__read_xls_range(cml_bench_path, start="V", stop="AO")

    def get_results_list_from_database(self, cml_bench_path):
        return self.__read_xls_range(cml_bench_path, start="AQ", stop="BJ")

    def get_reference_id_from_database(self, cml_bench_path):
        return self.__read_xls_range(cml_bench_path, start="U")

    def __read_xls_range(self, cml_bench_path, start, stop=None):
        xl = win32com.client.Dispatch("Excel.Application")
        xl.Visible = False
        wb = xl.Workbooks.Open(Filename=self.__database, ReadOnly=1)
        ws = wb.WorkSheets("Path")

        if stop:
            result = []
        else:
            result = None
        cols = [c.value for c in ws.Range("A2:T2")]
        i = 2
        while i < 1000:
            j = 1
            while j <= 20:
                val = ws.cells(i, j).value
                if val:
                    cols[j - 1] = val
                    k = j + 1
                    while k <= 20:
                        cols[k - 1] = None
                        k += 1
                    break
                j += 1
                if j > 20:
                    terminal.show_error_message("Database error. Path not found")
                    wb.Close()
                    return result
            path = '/'.join(col for col in cols if col)
            if path == cml_bench_path:
                if stop:
                    result = [f.value for f in ws.Range(start + str(i) + ":" + stop + str(i)) if f.value]
                else:
                    result = ws.Range(start + str(i)).value
                break
            i += 1
        wb.Close()
        return result
