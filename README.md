# telegram-bot
Este es un bot de Telegram programado en Python. 

# Características
    * Menú principal:
        * Consultar el clima con OpenWeatherMap y OpenAI
        * Contar añadiendo una unidad a un contador persistido por usuario
        * Analizar sentimiento de la conversación con OpenAI
    
    * Reconocimiento de mensajes de voz:
        Considero que mejora la experiencia del usuario porque la comunicación a través de mensages de voz es muy usada y añade una forma más ágil de hacer pedidos al bot. 
        Además de que puede mejorar la accesibilidad para usuarios con facultades motoras restringidas. 
    
    * Consultas directas a OpenAI:
        También agregué la posibilidad de realizar consultas a Open AI para poder tener conversaciones más ricas a la hora de utilizar la funcionalidad de analizar el sentimiento de la conversación. 
    
    * Localización:
        Facilita la posibilidad de que el bot pueda ser utilizado por personas que hablan distintos lenguajes.
        Nota: Para cambiar la localización, es necesario ir al achivo \config\constants.py y cambiar el valor de la constante CURRENT_LANGUAGE a alguno de los lenguajes soportados.
        Actualmente "es" o "en" para español o inglés respectivamente.


# Instalación
## Requisitos previos
    * Requiere Python 3.11.8 o posterior.
    * Telegram Bot API token (Necesitas crear un bot de telegram con @BotFather: https://core.telegram.org/bots/features#creating-a-new-bot)
    * Open Weather Map API key (https://openweathermap.org/)
    * OpenAI API key (https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)

## Dependencias
    Todas las dependencias se encuentran en el archivo requirements.txt

## Referencias a API keys
    El projecto incluye un archivo '.env.example', que debe ser copiado y renombrado a '.env'
    Dentro de este archivo, deben colocarse las API keys obtenidas previamente.

## Instrucciones
    1. Instala las dependencias necesarias ejecutando el siguiente comando desde la carpeta raiz del proyecto:
        pip install -r requirements.txt
    2. i. Copia el archivo '.env.example' y renombrarlo a '.env'.
       ii. Reemplaza los valores de las variables dentro del archivo por las API keys obtenidas previamente.
    3. i. Ve a telegram, a la conversación con @BotFather.
       ii. Envía el comando \setcommands.
       iii. Selecciona el bot al que le quieras modificar la lista de comandos.
       iv. Envía el siguiente mensaje: "start - Inicia el bot"
    4. Ejecutar main.py con python/python3
        python main.py
        o
        python3 main.py
    5. Inicia una conversación con tu Bot utilizando el comando /start desde el botón Menú o escribiéndolo como mensaje
    

