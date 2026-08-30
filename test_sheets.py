from sheets_client import get_medicamentos

datos = get_medicamentos()
print(f"Se encontraron {len(datos)} medicamentos:")
for med in datos:
    print(med)