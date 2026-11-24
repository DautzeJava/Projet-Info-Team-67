def create_building(building_type, position):
    positions = int(input(f"Entrez la position de la {building_type} (0 à 9) : "))
    return {"type": building_type, "position": positions}