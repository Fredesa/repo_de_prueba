import json
import os
import re
import requests

### Funciones

## Funcion de buscar texto en variable issue_body
def search_text(name_input):
    descripcion = ""
    descripcion_match = re.search(fr"### {name_input}\s*(.*)", issue_body, re.DOTALL)
    if descripcion_match:
        descripcion = descripcion_match.group(1).strip()
        descripcion = descripcion.split("###")[0].strip()
    else: descripcion = None
    return descripcion
    
## Variables de entorno
issue_body = os.getenv("ISSUE_BODY", "Cuerpo no disponible")
new_label = os.getenv("NEW_LABEL", "Nuevo label no disponible")


## Variables locales
azure_id = search_text("Codigo Azure:")

### Cuerpos de Peticiones

##Cuerpo de Peticion de Issue en Azure
headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": "Bearer DpvcWcHsEn4QbADZJtyOJdS3723LZLfpvapBu2GhZSOBYE8l50HrJQQJ99ALACAAAAAFtioVAAASAZDODPmh"
}

### Funciones de Peticiones
def updateTag(tag):
    body_add_tag = [
        {
            "op": "add",
            "path": "/fields/System.Tags",
            "value": f"{tag}"
        }
    ]
    resp = requests.patch(f"https://dev.azure.com/GrupoBancolombia/Vicepresidencia%20Servicios%20de%20Tecnología/_apis/wit/workitems/{azure_id}?api-version=7.1-preview.3", json=body_add_tag, headers=headers)
    print(f"Actualizacion de Tag:{resp.content}")


def updateArea(route):
    body_update_area = [
        {
            "op": "update",
            "path": "/fields/System.AreaPath",
            "value": f"Vicepresidencia Servicios de Tecnología\\Distribución\\EVC - GALATEA MODERNIZACION DE CANALES\\{route}"
        }
    ]
    resp = requests.patch(f"https://dev.azure.com/GrupoBancolombia/Vicepresidencia%20Servicios%20de%20Tecnología/_apis/wit/workitems/{azure_id}?api-version=7.1-preview.3", json=body_update_area, headers=headers)
    print(f"Actualizacion de Area:{resp.content}")

print(azure_id)
match new_label:
    case "PO":
        updateTag(" PO")
    case "P1":
        updateTag(" P1")
    case "P2":
        updateTag(" P2")
    case "P3":
        updateTag(" P3")
    case "team-soporte":
        updateArea("EQU0907 - ATLAS")
    case "team-financieros":
        updateArea("EQU0825 - VANAHEIM")
    case _:
        print("El tag no genera actualizacion")
        
    
