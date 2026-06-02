# -*- coding: utf-8 -*-
"""
Cria a pasta data/database_tiny com apenas os 28 arquivos de vibracao
efetivamente utilizados no trabalho final, preservando a estrutura de diretorios
original. O dataset completo ocupa ~80 GB; o tiny ocupa ~7 GB.

Uso:
    python construir_dataset_tiny.py

O script le a configuracao de config.py pra saber exatamente quais arquivos
sao necessarios, entao qualquer mudanca nos modos de falha e automaticamente
refletida aqui.
"""
import os
import shutil
import config


# destino do dataset reduzido
DESTINO = os.path.join(config.RAIZ, "..", "data", "database_tiny")


def lp(caminho):
    """Prefixo de caminho estendido do Windows (caminhos > 260 chars)."""
    caminho = os.path.abspath(caminho)
    return caminho if caminho.startswith("\\\\?\\") else "\\\\?\\" + caminho


def copiar(origem, destino):
    """Copia um arquivo garantindo que o diretorio de destino existe."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if os.path.exists(destino):
        return False  # ja existe, nao recopia
    shutil.copy2(lp(origem), lp(destino))
    return True


def listar_arquivos_necessarios():
    """Percorre os modos de config.py e lista todos os arquivos CSV necessarios."""
    arquivos = []
    for modo in config.MODOS:
        motor, vel, canal = modo["motor"], modo["vel"], modo["canal"]
        condicoes = list(modo["healthy"]) + list(modo["severidades"])
        for cond in condicoes:
            nome = "Vibration_Motor-%d_%d_time-%s-ch%d.csv" % (motor, vel, cond, canal)
            origem = os.path.join(
                config.DATASET, "Vibration",
                "Motor-%d" % motor, str(vel), cond, nome)
            # caminho relativo dentro do dataset (para reconstruir no destino)
            rel = os.path.join("Vibration", "Motor-%d" % motor, str(vel), cond, nome)
            arquivos.append((origem, rel, modo["id"], cond))
    # remove duplicatas (o mesmo arquivo healthy pode ser compartilhado entre modos)
    vistos = set()
    unicos = []
    for item in arquivos:
        if item[1] not in vistos:
            vistos.add(item[1])
            unicos.append(item)
    return unicos


def main():
    arquivos = listar_arquivos_necessarios()
    print("Arquivos necessarios: %d" % len(arquivos))
    print("Destino: %s" % DESTINO)
    print()

    # confere se os arquivos de origem existem
    ausentes = [a for a in arquivos if not os.path.exists(lp(a[0]))]
    if ausentes:
        print("AVISO: %d arquivos nao encontrados na origem:" % len(ausentes))
        for a in ausentes:
            print("  FALTANDO: %s" % a[1])
        print()

    # copia os arquivos presentes
    copiados = 0
    ja_existia = 0
    total_bytes = 0
    for origem, rel, modo_id, cond in arquivos:
        if not os.path.exists(lp(origem)):
            continue
        destino = os.path.join(DESTINO, rel)
        novo = copiar(origem, destino)
        tam = os.path.getsize(lp(origem))
        total_bytes += tam
        if novo:
            copiados += 1
            print("  Copiado [%s / %s] (%.0f MB)" % (modo_id, cond, tam / 1e6))
        else:
            ja_existia += 1

    print()
    print("Concluido.")
    print("  Copiados agora : %d arquivos" % copiados)
    print("  Ja existiam    : %d arquivos" % ja_existia)
    print("  Total no tiny  : %.1f GB" % (total_bytes / 1e9))
    print()
    print("Para usar o dataset tiny, edite config.py e aponte DATASET para:")
    print("  %s" % os.path.join(DESTINO, "Vibration").replace("\\", "/"))
    print("  (substitua a variavel DATASET na linha correspondente)")


if __name__ == "__main__":
    main()
