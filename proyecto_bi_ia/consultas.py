import pandas as pd
from conexion import ejecutar_consulta, obtener_conexion


def limpiar_texto(valor):
    if valor is None:
        return None
    return str(valor).replace("'", "''")


def construir_filtros(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    condiciones = []

    if anio and anio != "Todos":
        condiciones.append(f"t.ano_eje = {int(anio)}")

    if sector and sector != "Todos":
        sector = limpiar_texto(sector)
        condiciones.append(f"s.sector_nombre = '{sector}'")

    if departamento and departamento != "Todos":
        departamento = limpiar_texto(departamento)
        condiciones.append(f"u.departamento_ejecutora_nombre = '{departamento}'")

    if nivel and nivel != "Todos":
        nivel = limpiar_texto(nivel)
        condiciones.append(f"ng.nivel_gobierno_nombre = '{nivel}'")

    if fuente and fuente != "Todos":
        fuente = limpiar_texto(fuente)
        condiciones.append(f"f.fuente_financiamiento_nombre = '{fuente}'")

    if condiciones:
        return "WHERE " + " AND ".join(condiciones)

    return ""


def obtener_anios():
    query = """
    SELECT DISTINCT t.ano_eje
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    WHERE t.ano_eje IS NOT NULL
    ORDER BY t.ano_eje;
    """
    return ejecutar_consulta(query)


def obtener_sectores(anio="Todos"):
    filtro = construir_filtros(anio=anio)

    query = f"""
    SELECT DISTINCT s.sector_nombre
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    {filtro}
    ORDER BY s.sector_nombre;
    """
    return ejecutar_consulta(query)


def obtener_departamentos(anio="Todos", sector="Todos"):
    filtro = construir_filtros(anio=anio, sector=sector)

    query = f"""
    SELECT DISTINCT u.departamento_ejecutora_nombre
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    {filtro}
    ORDER BY u.departamento_ejecutora_nombre;
    """
    return ejecutar_consulta(query)


def obtener_niveles_gobierno(anio="Todos", sector="Todos", departamento="Todos"):
    filtro = construir_filtros(
        anio=anio,
        sector=sector,
        departamento=departamento
    )

    query = f"""
    SELECT DISTINCT ng.nivel_gobierno_nombre
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    {filtro}
    ORDER BY ng.nivel_gobierno_nombre;
    """
    return ejecutar_consulta(query)


def obtener_fuentes_financiamiento(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos"):
    filtro = construir_filtros(
        anio=anio,
        sector=sector,
        departamento=departamento,
        nivel=nivel
    )

    query = f"""
    SELECT DISTINCT f.fuente_financiamiento_nombre
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    ORDER BY f.fuente_financiamiento_nombre;
    """
    return ejecutar_consulta(query)


def indicadores_generales(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        COALESCE(SUM(h.monto_pia), 0) AS total_pia,
        COALESCE(SUM(h.monto_pim), 0) AS total_pim,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado,
        COALESCE(SUM(h.monto_girado), 0) AS total_girado,
        COALESCE(
            ROUND(SUM(h.monto_devengado) / NULLIF(SUM(h.monto_pim), 0) * 100, 2),
            0
        ) AS avance_porcentaje
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro};
    """
    return ejecutar_consulta(query)


def gasto_por_anio(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        t.ano_eje,
        COALESCE(SUM(h.monto_pia), 0) AS total_pia,
        COALESCE(SUM(h.monto_pim), 0) AS total_pim,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado,
        COALESCE(SUM(h.monto_girado), 0) AS total_girado
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY t.ano_eje
    ORDER BY t.ano_eje;
    """
    return ejecutar_consulta(query)


def gasto_por_sector(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        s.sector_nombre,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY s.sector_nombre
    ORDER BY total_devengado DESC
    LIMIT 10;
    """
    return ejecutar_consulta(query)


def gasto_por_departamento(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        u.departamento_ejecutora_nombre,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY u.departamento_ejecutora_nombre
    ORDER BY total_devengado DESC
    LIMIT 10;
    """
    return ejecutar_consulta(query)


def gasto_por_financiamiento(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        f.fuente_financiamiento_nombre,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY f.fuente_financiamiento_nombre
    ORDER BY total_devengado DESC;
    """
    return ejecutar_consulta(query)


def gasto_por_nivel_gobierno(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        ng.nivel_gobierno_nombre,
        COALESCE(SUM(h.monto_pim), 0) AS total_pim,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado,
        COALESCE(SUM(h.monto_girado), 0) AS total_girado
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY ng.nivel_gobierno_nombre
    ORDER BY total_devengado DESC;
    """
    return ejecutar_consulta(query)


def consulta_integrada(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    filtro = construir_filtros(anio, sector, departamento, nivel, fuente)

    query = f"""
    SELECT 
        t.ano_eje,
        s.sector_nombre,
        u.departamento_ejecutora_nombre,
        ng.nivel_gobierno_nombre,
        f.fuente_financiamiento_nombre,
        f.rubro_nombre,
        COALESCE(SUM(h.monto_pia), 0) AS total_pia,
        COALESCE(SUM(h.monto_pim), 0) AS total_pim,
        COALESCE(SUM(h.monto_devengado), 0) AS total_devengado,
        COALESCE(SUM(h.monto_girado), 0) AS total_girado,
        COALESCE(
            ROUND(SUM(h.monto_devengado) / NULLIF(SUM(h.monto_pim), 0) * 100, 2),
            0
        ) AS avance_porcentaje
    FROM hecho_gasto_reactivacion h
    INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
    INNER JOIN dim_sector s ON h.id_sector = s.id_sector
    INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
    INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
    INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
    {filtro}
    GROUP BY 
        t.ano_eje,
        s.sector_nombre,
        u.departamento_ejecutora_nombre,
        ng.nivel_gobierno_nombre,
        f.fuente_financiamiento_nombre,
        f.rubro_nombre
    ORDER BY total_devengado DESC
    LIMIT 200;
    """
    return ejecutar_consulta(query)


def serie_temporal_prediccion(anio="Todos", sector="Todos", departamento="Todos", nivel="Todos", fuente="Todos"):
    conn = obtener_conexion()

    sql = """
        SELECT
            t.ano_eje,
            t.mes_eje,
            COALESCE(SUM(h.monto_pia), 0) AS total_pia,
            COALESCE(SUM(h.monto_pim), 0) AS total_pim,
            COALESCE(SUM(h.monto_devengado), 0) AS total_devengado,
            COALESCE(SUM(h.monto_girado), 0) AS total_girado
        FROM hecho_gasto_reactivacion h
        INNER JOIN dim_tiempo t ON h.id_tiempo = t.id_tiempo
        INNER JOIN dim_sector s ON h.id_sector = s.id_sector
        INNER JOIN dim_ubigeo u ON h.id_ubigeo = u.id_ubigeo
        INNER JOIN dim_nivel_gobierno ng ON h.id_nivel_gobierno = ng.id_nivel_gobierno
        INNER JOIN dim_financiamiento f ON h.id_financiamiento = f.id_financiamiento
        WHERE 1 = 1
    """

    if anio and anio != "Todos":
        sql += f" AND t.ano_eje = {int(anio)} "

    if sector and sector != "Todos":
        sector = limpiar_texto(sector)
        sql += f" AND s.sector_nombre = '{sector}' "

    if departamento and departamento != "Todos":
        departamento = limpiar_texto(departamento)
        sql += f" AND u.departamento_ejecutora_nombre = '{departamento}' "

    if nivel and nivel != "Todos":
        nivel = limpiar_texto(nivel)
        sql += f" AND ng.nivel_gobierno_nombre = '{nivel}' "

    if fuente and fuente != "Todos":
        fuente = limpiar_texto(fuente)
        sql += f" AND f.fuente_financiamiento_nombre = '{fuente}' "

    sql += """
        GROUP BY t.ano_eje, t.mes_eje
        ORDER BY t.ano_eje, t.mes_eje;
    """

    df = pd.read_sql(sql, conn)
    conn.close()
    return df