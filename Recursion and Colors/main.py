# Función principal que resuelve el problema de las varillas con restricciones de color
def varilla_color(n, disks):
    # Inicialización de las tres varillas como listas
    source = [(size, color) for size, color in disks]  # Varilla origen (A)
    auxiliary = []  # Varilla auxiliar (B)
    destination = []  # Varilla destino (C)
    moves = []  # Almacenará los movimientos solución
    
    # Función recursiva que implementa el algoritmo
    def move_disks(num_disks, source_rod, target_rod, aux_rod, source_name, target_name, aux_name):
        # Caso base: si no hay discos para mover, termina la recursión
        if num_disks == 0:
            return True
        
        # Paso 1: Mover n-1 discos de origen a auxiliar (llamada recursiva)
        if not move_disks(num_disks - 1, source_rod, aux_rod, target_rod, source_name, aux_name, target_name):
            return False
        
        # Paso 2: Mover el disco actual (el más grande) a destino
        if source_rod:
            disk_to_move = source_rod[-1]  # Toma el disco superior
            
            # Verifica restricciones:
            # 1. No puede colocar disco más grande sobre uno más pequeño
            # 2. No puede colocar disco sobre otro del mismo color
            if target_rod:
                top_target = target_rod[-1]
                if disk_to_move[0] > top_target[0] or disk_to_move[1] == top_target[1]:
                    return False  # Movimiento inválido
            
            # Realiza el movimiento si pasa las validaciones
            moved_disk = source_rod.pop()  # Remueve disco de origen
            target_rod.append(moved_disk)  # Coloca en destino
            moves.append((moved_disk[0], source_name, target_name))  # Registra movimiento
            
            # Paso 3: Mover n-1 discos de auxiliar a destino (llamada recursiva)
            if not move_disks(num_disks - 1, aux_rod, target_rod, source_rod, aux_name, target_name, source_name):
                return False
        
        return True  # Si todas las llamadas recursivas son exitosas
    
    # Intenta resolver el problema
    if move_disks(n, source, destination, auxiliary, 'A', 'C', 'B'):
        return moves  # Retorna la lista de movimientos si tiene solución
    else:
        return -1  # Retorna -1 si no hay solución válida

# Función para obtener y validar números enteros
def obtener_entero(mensaje, min_val=1, max_val=8):
    while True:
        try:
            valor = int(input(mensaje))
            if min_val <= valor <= max_val:
                return valor
            print(f"Error: Ingrese un número entre {min_val} y {max_val}")
        except ValueError:
            print("Error: Debe ser un número entero")

# Función para estandarizar formatos de color
def estandarizar_color(color):
    """Convierte a minúsculas y elimina todos los espacios"""
    return color.lower().strip().replace(" ", "")

# Función para obtener y validar colores
def obtener_color(mensaje):
    while True:
        color = input(mensaje)
        color_estandarizado = estandarizar_color(color)
        if color_estandarizado:
            return color_estandarizado
        print("Error: El color no puede estar vacío")

# Función principal que maneja el flujo del programa
def main():
    print("\n=== VARILLAS CON RESTRICCIONES DE COLOR ===")
    print("Ingrese los datos solicitados:")
    
    # Obtener número de discos (validado)
    n = obtener_entero("\nNúmero de discos (1-8): ")
    disks = []  # Almacenará los discos ingresados
    
    # Ingresar datos para cada disco
    print("\nIngrese los discos (empezando por el más grande):")
    for i in range(n):
        print(f"\nDisco {i+1}:")
        size = obtener_entero(f"  Tamaño (debe ser {n-i} para orden descendente): ", 1, 100)
        color = obtener_color("  Color: ")
        disks.append((size, color))
    
    # Ordenar discos por tamaño (de mayor a menor)
    disks.sort(reverse=True, key=lambda x: x[0])
    
    # Mostrar discos ingresados (con colores estandarizados)
    print("\nDiscos ingresados (tamaño, color):")
    for size, color in disks:
        print(f"  ({size}, '{color}')")
    
    # Resolver el problema
    print("\nResultado:")
    result = varilla_color(n, disks)
    
    # Mostrar resultados
    if result == -1:
        print("-1 (Imposible resolver el problema con las entradas dadas)")
    else:
        for move in result:
            print(f"({move[0]}, '{move[1]}', '{move[2]}')")

# Punto de entrada del programa
if __name__ == "__main__":
    main()