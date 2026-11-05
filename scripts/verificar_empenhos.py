#!/usr/bin/env python3
"""Verificação diária da integridade da base de empenhos.

A consulta automatizada não é habilitada antes da validação dos endpoints oficiais.
Não interpreta base vazia como ausência de novos empenhos.
"""
import json
from pathlib import Path
from datetime import date

p = Path("dados/empenhos.json")
data = json.loads(p.read_text(encoding="utf-8"))
assert data["inicio_monitoramento"] == "2026-11-05"
assert isinstance(data["empenhos"], list)
assert set(data["fontes"]) == {"SEDUC", "SEMED"}
if not data.get("validado"):
    print("PENDENTE: fontes de empenhos ainda não validadas; nenhum dado foi coletado.")
    print("Não publicar zero empenhos como resultado confirmado.")
else:
    seen=set()
    for e in data["empenhos"]:
        assert e["orgao"] in {"SEDUC", "SEMED"}
        assert e["data"] >= "2026-11-05"
        assert isinstance(e["valor"], (int,float))
        k=(e["orgao"],e["empenho"])
        assert k not in seen, "Empenho duplicado"
        seen.add(k)
    print(f"Base validada: {len(seen)} empenhos")
