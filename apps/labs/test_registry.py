from labs.registry import LABORATORIOS
print('Laboratorios registrados:')
for key, value in LABORATORIOS.items():
    print(f'  {key}: {value[\
nombre\]}')
    print(f'    Directorio: {value[\compose_dir\]}')
    print(f'    Servicio: {value[\service\]}')
    print(f'    URL: {value[\url\]}')
