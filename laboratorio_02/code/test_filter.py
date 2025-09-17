#!/usr/bin/env python3
"""
Script de teste para verificar a filtragem do class.csv
"""

from auto_cloning import filter_class_csv

# Testa a filtragem no repositório spring-boot
print("Testando filtragem do class.csv para spring-boot...")
filter_class_csv('spring-boot')
print("Teste concluído!")
