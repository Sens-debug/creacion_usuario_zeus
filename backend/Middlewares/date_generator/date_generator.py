from datetime import datetime
from dateutil.relativedelta import relativedelta
def date_generator_parser():
    try:
        # Fecha actual
        fecha_actual = datetime.now()

        # Fecha 6 meses después
        fecha_6_meses_despues = fecha_actual + relativedelta(months=6)

        # Formatear fechas en yyyy/mm/dd
        formato = "%Y/%m/%d"
        fecha_actual_str = fecha_actual.strftime(formato)
        fecha_6_meses_str = fecha_6_meses_despues.strftime(formato)

        return [fecha_actual_str,fecha_6_meses_str]
    except Exception as e:
        return [e]
