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
  
## Funcion que limpia el url para poder enviar la ruta del Issue
def limpiar_url(url):
    patron = r'^https://api\.github\.com/repos/'
    return re.sub(patron, '', url)
  
## Funcion que extrae el id del Issue de la ruta 
def extraer_id_final(url):
    patron = r'.*/(\d+)$'
    match = re.search(patron, url)
    return match.group(1) if match else None
  
### Variables

## Variables de entorno
issue_title = os.getenv("ISSUE_TITLE", "Título no disponible")
issue_body = os.getenv("ISSUE_BODY", "Cuerpo no disponible")
issue_url = os.getenv("ISSUE_URL", "Direccion no disponible")
repo_name = os.getenv("REPO_NAME","Nombre no disponible")


## Variables locales
descripcion_issue = search_text("Describa el error")
replicar_issue= search_text("Como replicar el error")
nombre_del_componente = search_text("Nombre del componente") if search_text("Nombre del componente") != None else repo_name
version = search_text("Version del componente Galatea")
programa = search_text("Programa") if search_text("Programa") != None else search_text("EVC")
evidencias = search_text("Adjunte Evidencias")
clasificacion = "Mobile" if repo_name.find('MOBILE') != -1 else "Web"
id_issue_github = extraer_id_final(issue_url)
issue_route = limpiar_url(issue_url)

description_azure = f"""
    <strong>Descripcion:</strong>
    <br>{descripcion_issue} <br>
    <br>
    <strong>Como replicar el error:</strong>
    <br>{replicar_issue} <br>
    <br>
    <strong>Version:</strong>
    <br>{version} <br>
    <br>
    <strong>Link:</strong>
    <br>https://github.com/{issue_route}
"""

criterios_azure = """
* Realizar un primer contacto con el usuario oportunamente</br>
* Solucionar el incidente mencionado en desarrollo.</br>
* Hacer las respectivas pruebas al componente.</br>
* Realizar PR en LTS y Trunk (Artifactory)</br>
* PR aceptado y versión disponibilizada.</br>
* Lanzar release para disponibilizar versión en S3.</br>
* Lanzar comunicado en grupo de Teams</br>
* Certificación del Issue: creación DoD creacion del test plan.</br>
* Documentar en Sharepoint, dejar registro en comentarios, cerrar el issue.</br>
* Documentar el issue de forma clara</br>
* Adjuntar evidencias de lo trabajado (si es posible pantallazos de parte del usuario)</br>
* Crear tareas descriptivas</br>
* Relacionar los:</br>
     - PRs</br>
     - Releases (si aplica)</br>
"""
prioridad = "ALTO" if programa == 'SVN' or programa == 'SVP' or programa == 'APP' else "BAJO"


### Cuerpos de Peticiones

##Cuerpo de Peticion de Issue en Azure
headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": "Bearer DpvcWcHsEn4QbADZJtyOJdS3723LZLfpvapBu2GhZSOBYE8l50HrJQQJ99ALACAAAAAFtioVAAASAZDODPmh"
}

body_request= [
  {
    "op": "add",
    "path": "/fields/System.AreaPath",
    "value": "Vicepresidencia Servicios de Tecnología\\Distribución\\EVC - GALATEA MODERNIZACION DE CANALES\\EQU0907 - ATLAS"
  },
  {
    "op": "add",
    "path": "/fields/System.IterationPath",
    "value": "Vicepresidencia Servicios de Tecnología\\2025"
  },
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": f"[{clasificacion}]({nombre_del_componente}): {issue_title}"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": f"{description_azure}"
  },
  {
    "op": "add",
    "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
    "value": f"{criterios_azure}"
  },
  {
    "op": "add",
    "path": "/fields/System.Tags",
    "value": f"{clasificacion}; {programa}; {prioridad} "
  },
  {
    "op": "add",
    "path": "/fields/System.AttachedFiles",
    "value": f"{evidencias}"
  },
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "System.LinkTypes.Hierarchy-Reverse",
      "url": f"https://dev.azure.com/GrupoBancolombia/Vicepresidencia%20Servicios%20de%20Tecnología/_apis/wit/workitems/6129179",
      "attributes": {
        "comment": "Estableciendo el work item padre"
      }
    }
  }
]



### Peticiones

##Evento de generacion de issue en Azure
resp = requests.post(f"https://dev.azure.com/GrupoBancolombia/Vicepresidencia%20Servicios%20de%20Tecnología/_apis/wit/workitems/$issue?api-version=7.1-preview.3", json=body_request, headers=headers)

## Optencion de ID de Issue en Azure DevOps
resp_string = json.loads(resp.content)
codigo_azure = resp_string['id']

##Cuerpo de Peticion de mensaje en teams
body_request_teams= {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": [
                  {
                      "type": "TextBlock",
                      "size": "medium",
                      "weight": "bolder",
                      "text": "Hola compañeros de Soporte Mobile",
                      "style": "heading",
                        "wrap": "true"
                  },
                  {
                        "type": "FactSet",
                        "facts": [
                            {
                                "title": "Titulo del caso: ",
                                "value": f"{issue_title}"
                            },
                            {
                                "title": "Nombre de componente: ",
                                "value": f"{nombre_del_componente}"
                            },
                            {
                                "title": "Programa/EVC: ",
                                "value": f"{programa}"
                            },
                            {
                                "title": "Version: ",
                                "value": f"{version}"
                            },
                            {
                                "title": "Vinculo de azure: ",
                                "value": f"https://dev.azure.com/GrupoBancolombia/Vicepresidencia%20Servicios%20de%20Tecnolog%C3%ADa/_workitems/edit/{codigo_azure}"
                            },
                            {
                                "title": "Vinculo de Github: ",
                                "value": f"https://github.com/{issue_route}"
                            }
                        ]
                    },
              ],
            }
        }
    ]
}

## Generacion de texto para que se añada en github
codigo_azure_github = {
    "body": f"""
    {body_request}
    
    ### Codigo Azure:

    {codigo_azure}
    """
}
##Evento de actualizacion de datos en Github

respUpdateGithub = requests.patch(f"{issue_url}",json=codigo_azure_github)

##Evento de generacion de issue en Azure
respTeams = requests.post(f"https://prod-41.westus.logic.azure.com:443/workflows/3b6817637bf0410291d94180ed92381b/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=29rs208Kx9Adod43QwAgS7WxjgNPLf4TRf4r5kY7Ps0", json=body_request_teams)

print(resp)
print(respTeams)

    
