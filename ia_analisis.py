from sklearn.linear_model import LinearRegression


def formato_soles(valor):
    valor = valor or 0
    return f"S/ {valor:,.2f}"


def interpretar_indicadores(total_pim, total_devengado, total_girado, avance):
    total_pim = total_pim or 0
    total_devengado = total_devengado or 0
    total_girado = total_girado or 0
    avance = avance or 0

    texto = (
        f"Observa este primer resumen. El Presupuesto Institucional Modificado alcanza {formato_soles(total_pim)}. "
        f"De ese total, se ha devengado {formato_soles(total_devengado)} y se ha girado {formato_soles(total_girado)}. "
        f"El avance devengado es de {avance:.2f}%. "
    )

    if avance >= 80:
        texto += (
            "Esto indica una ejecución alta. En términos de gestión pública, significa que gran parte del presupuesto "
            "ya pasó a la etapa de reconocimiento de obligación de pago."
        )
    elif avance >= 50:
        texto += (
            "Esto indica una ejecución media. Es recomendable revisar qué sectores o departamentos concentran menor avance "
            "para identificar posibles retrasos."
        )
    else:
        texto += (
            "Esto indica una ejecución baja. Puede reflejar retrasos en la programación, certificación, compromiso o devengado del gasto."
        )

    return texto


def explicar_grafico_anual(df):
    if df.empty:
        return "No hay datos suficientes para explicar la evolución anual."

    mejor = df.loc[df["total_devengado"].idxmax()]
    menor = df.loc[df["total_devengado"].idxmin()]

    texto = (
        f"En el gráfico de evolución anual, la IA identifica que el año con mayor gasto devengado es {int(mejor['ano_eje'])}, "
        f"con {formato_soles(mejor['total_devengado'])}. "
        f"El año con menor gasto devengado es {int(menor['ano_eje'])}, con {formato_soles(menor['total_devengado'])}. "
        "Este gráfico permite observar la tendencia del gasto de reactivación económica a lo largo del tiempo."
    )

    return texto


def explicar_grafico_sector(df):
    if df.empty:
        return "No hay datos suficientes para explicar el gráfico por sectores."

    principal = df.iloc[0]
    texto = (
        f"En el ranking por sectores, el sector que lidera el gasto devengado es {principal['sector_nombre']}, "
        f"con {formato_soles(principal['total_devengado'])}. "
        "Esto significa que dicho sector concentra la mayor participación en la ejecución del gasto analizado. "
        "Si el gráfico muestra una gran diferencia entre el primer sector y los demás, existe una concentración del gasto."
    )

    return texto


def explicar_grafico_departamento(df):
    if df.empty:
        return "No hay datos suficientes para explicar el gráfico por departamentos."

    principal = df.iloc[0]
    texto = (
        f"En el gráfico por departamentos, el mayor gasto devengado se concentra en {principal['departamento_ejecutora_nombre']}, "
        f"con {formato_soles(principal['total_devengado'])}. "
        "Este resultado permite identificar qué territorio concentra mayor ejecución presupuestal dentro del periodo o filtro seleccionado."
    )

    return texto


def explicar_grafico_financiamiento(df):
    if df.empty:
        return "No hay datos suficientes para explicar la fuente de financiamiento."

    principal = df.iloc[0]
    texto = (
        f"En la distribución por fuente de financiamiento, la principal fuente es {principal['fuente_financiamiento_nombre']}, "
        f"con {formato_soles(principal['total_devengado'])}. "
        "Esta lectura ayuda a comprender de dónde provienen los recursos que financian el gasto de reactivación económica."
    )

    return texto


def explicar_grafico_nivel(df):
    if df.empty:
        return "No hay datos suficientes para explicar el nivel de gobierno."

    principal = df.iloc[0]
    texto = (
        f"En el análisis por nivel de gobierno, el mayor gasto devengado corresponde a {principal['nivel_gobierno_nombre']}, "
        f"con {formato_soles(principal['total_devengado'])}. "
        "Esto permite comparar la participación entre gobierno nacional, regional o local."
    )

    return texto


def generar_clase_ia(df_anio, df_sector, df_departamento, df_financiamiento, df_nivel, total_pim, total_devengado, total_girado, avance):
    texto = "Te explicaré el dashboard paso a paso. "
    texto += interpretar_indicadores(total_pim, total_devengado, total_girado, avance) + " "
    texto += explicar_grafico_anual(df_anio) + " "
    texto += explicar_grafico_sector(df_sector) + " "
    texto += explicar_grafico_departamento(df_departamento) + " "
    texto += explicar_grafico_financiamiento(df_financiamiento) + " "
    texto += explicar_grafico_nivel(df_nivel)

    return texto


def responder_pregunta_usuario(pregunta, df_anio, df_sector, df_departamento, df_financiamiento, df_nivel):
    pregunta = pregunta.lower()

    if "año" in pregunta or "anio" in pregunta or "evolución" in pregunta:
        return explicar_grafico_anual(df_anio)

    if "sector" in pregunta:
        return explicar_grafico_sector(df_sector)

    if "departamento" in pregunta or "region" in pregunta or "región" in pregunta:
        return explicar_grafico_departamento(df_departamento)

    if "financiamiento" in pregunta or "fuente" in pregunta:
        return explicar_grafico_financiamiento(df_financiamiento)

    if "gobierno" in pregunta or "nivel" in pregunta:
        return explicar_grafico_nivel(df_nivel)

    return (
        "Puedo ayudarte a interpretar la evolución anual, los sectores, departamentos, fuentes de financiamiento "
        "o niveles de gobierno. Escribe, por ejemplo: explícame el sector con mayor gasto."
    )


def predecir_gasto_siguiente_anio(df_anio):
    datos = df_anio.dropna()

    if len(datos) < 2:
        return None, None

    X = datos[["ano_eje"]]
    y = datos["total_devengado"]

    modelo = LinearRegression()
    modelo.fit(X, y)

    siguiente_anio = int(datos["ano_eje"].max() + 1)
    prediccion = modelo.predict([[siguiente_anio]])[0]

    return siguiente_anio, prediccion