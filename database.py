import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database=os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )


def salvar_leitura(dados):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO weather_readings (
            estacao,
            data_hora,
            temperatura_c,
            umidade_pct,
            pressao_hpa,
            pressao_nivel_mar_hpa,
            altitude_m,
            uv_indice,
            uv_raw,
            tendencia
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        dados.get("id"),
        dados.get("ts"),
        dados.get("temp_c"),
        dados.get("hum_pct"),
        dados.get("press_hpa"),
        dados.get("press_sl"),
        dados.get("alt_m"),
        dados.get("uv_idx"),
        dados.get("uv_raw"),
        dados.get("trend")
    )

    try:
        cursor.execute(sql, valores)
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()