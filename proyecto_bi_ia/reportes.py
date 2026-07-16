import io
import pandas as pd


def generar_excel_reportes(dfs):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for nombre_hoja, df in dfs.items():
            nombre_hoja = nombre_hoja[:31]
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)

    output.seek(0)
    return output