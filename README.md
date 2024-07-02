# Instrucciones para ejecutar el proyecto

## Configuración del entorno virtual

1. Abrir una terminal.
2. Crear y activar un entorno virtual:
     ```sh
     pip install virtualenv
     python -m venv venv
     en bash: source venv/Scripts/activate 
     ó en Windows . venv/Scripts/activate
     ```
3. Instalar las dependencias en \venv\Scripts\:
   - pip install -r requirements.txt
4. Finalmente ejecutar alexa.py
5. (Opcional) Actualizacion de dependencias en \:
    - pip freeze > requirements.txt