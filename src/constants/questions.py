#region Preguntas

questions = {
    # Preguntas fáciles
    "¿Cuál es el puerto predeterminado para HTTPS?\n1. 80\n2. 443\n3. 22\n4. 25": (2, 10),
    "¿Qué herramienta se utiliza comúnmente para realizar un escaneo de puertos en una red?\n1. Nmap\n2. Wireshark\n3. Metasploit\n4. Burp Suite": (1, 10),
    "¿Qué tipo de ataque implica la inserción de código malicioso en las consultas SQL?\n1. Cross-Site Scripting (XSS)\n2. Ataque de diccionario\n3. Inyección SQL\n4. Phishing": (3, 10),
    "¿Qué protocolo se utiliza para asegurar la comunicación en una red Wi-Fi?\n1. WEP\n2. WPA2\n3. WPA\n4. WPA3": (4, 10),
    "¿Qué significa 'DoS' en el contexto de ciberseguridad?\n1. Defacement of Service\n2. Denial of Service\n3. Data over Security\n4. Distribution of Service": (2, 10),
    "¿Cuál es el propósito de un firewall?\n1. Bloquear el acceso físico al servidor\n2. Monitorear y controlar el tráfico de red entrante y saliente\n3. Analizar y escanear vulnerabilidades\n4. Realizar copias de seguridad de datos": (2, 10),
    "¿Qué es una VPN?\n1. Virtual Public Network\n2. Virtual Private Network\n3. Visual Private Network\n4. Visual Public Network": (2, 10),
    "¿Qué es un ataque de fuerza bruta?\n1. Probar todas las combinaciones posibles de una clave\n2. Inyectar código malicioso\n3. Monitorear el tráfico de red\n4. Redirigir el tráfico de red a otro servidor": (1, 10),
    # Preguntas de dificultad media
    "¿Qué técnica utiliza el análisis de las frecuencias de uso de palabras o frases para decodificar mensajes cifrados?\n1. Fuerza bruta\n2. Criptoanálisis\n3. Ataque de diccionario\n4. Ingeniería social": (2, 20),
    "¿Cuál es el propósito del uso de un honeypot en una red?\n1. Aumentar la velocidad de la red\n2. Atraer y analizar comportamientos de atacantes\n3. Filtrar el tráfico de red\n4. Cifrar la comunicación": (2, 20),
    "¿Qué algoritmo de cifrado utiliza una clave pública y una clave privada para cifrar y descifrar datos?\n1. AES\n2. DES\n3. RSA\n4. MD5": (3, 20),
    "¿Cuál es la diferencia principal entre un ataque de tipo 'buffer overflow' y un 'heap overflow'?\n1. Ubicación en la memoria\n2. Tipo de datos afectados\n3. Tamaño del desbordamiento\n4. Modo de explotación": (1, 20),
    "¿Qué significa 'XSS' en el contexto de ciberseguridad?\n1. Cross-Site Scripting\n2. XML Secure Script\n3. Cross-Server Security\n4. Xtreme Secure Scripting": (1, 20),
    "¿Qué es una botnet?\n1. Una red de robots\n2. Una red de computadoras infectadas controladas remotamente\n3. Un programa para eliminar virus\n4. Una técnica de cifrado": (2, 20),
    "¿Qué protocolo se utiliza para cifrar correos electrónicos?\n1. SSL\n2. TLS\n3. PGP\n4. FTP": (3, 20),
    "¿Qué es un certificado digital?\n1. Un archivo que contiene virus\n2. Un documento que certifica la identidad de una persona o entidad\n3. Un protocolo de red\n4. Un algoritmo de cifrado": (2, 20),
    # Preguntas difíciles
    "¿Cuál es la longitud mínima recomendada para una clave RSA segura en la actualidad?\n1. 1024 bits\n2. 2048 bits\n3. 3072 bits\n4. 4096 bits": (2, 30),
    "¿Qué protocolo es utilizado por los sistemas de detección de intrusos basados en red (NIDS) para capturar y analizar el tráfico?\n1. SNMP\n2. NetFlow\n3. PCAP\n4. IPFIX": (3, 30),
    "¿Qué técnica criptográfica se utiliza en el protocolo TLS para asegurar la integridad y autenticidad de los datos?\n1. Criptografía asimétrica\n2. Funciones hash\n3. Cifrado simétrico\n4. Firmas digitales": (4, 30),
    "¿Cuál de los siguientes métodos es más seguro para el intercambio de claves en un entorno inseguro?\n1. Intercambio de claves Diffie-Hellman\n2. Intercambio de claves RSA\n3. Intercambio de claves ECC\n4. Intercambio de claves DSA": (3, 30),
    "¿Qué herramienta se utiliza para realizar fuzzing en aplicaciones con el objetivo de encontrar vulnerabilidades?\n1. Nessus\n2. Burp Suite\n3. AFL (American Fuzzy Lop)\n4. Nikto": (3, 30),
    "¿Cuál es el propósito del uso de un ataque de relleno de Oracle en criptografía?\n1. Descifrar datos cifrados sin la clave\n2. Insertar datos maliciosos en una base de datos\n3. Manipular la autenticación basada en tokens\n4. Detectar ataques de fuerza bruta": (1, 30),
    "¿Qué es un ataque de canal lateral?\n1. Un ataque que aprovecha información física del sistema\n2. Un ataque a través de la red\n3. Un ataque a la interfaz de usuario\n4. Un ataque a través de software de terceros": (1, 30),
    "¿Cuál es la diferencia entre 'salt' y 'pepper' en criptografía?\n1. Salt es una cadena aleatoria añadida a la entrada; Pepper es una cadena aleatoria añadida al hash\n2. Salt es una cadena fija; Pepper es una cadena aleatoria\n3. Salt se añade antes del hash; Pepper se añade después\n4. Salt se usa para cifrar datos; Pepper se usa para descifrar datos": (1, 30),
    # Preguntas de C y C++
    "¿Cómo se le llama a una variable que almacena la dirección en memoria de otra variable en C y C++?\n1. Parámetro\n2. Referencia\n3. Puntero\n4. Ninguna de las anteriores": (3, 20),
    "¿Cómo se imprime 'Hola mundo' en Java?\n1. System.out.println(\"Hola mundo\");\n2. std::cout << \"Hola mundo\"\n3. print(\"Hola mundo\")\n4. Console.WriteLine(\"Hola mundo\")": (1, 30),
    "¿Cómo se le llama al valor que se le pasa a una función?\n1. Parámetro\n2. Referencia\n3. Variable\n4. Argumento": (4, 25),
    "¿Qué es un array?\n1. Una lista de valores de un mismo tipo\n2. Una estructura de datos que asocia una clave y un valor\n3. Una estructura compuesta de nodos": (1, 20),
    "¿Qué es una instancia?\n1. Un valor retornado desde una función\n2. Un tipo de dato primitivo\n3. Un objeto creado a partir de una clase": (3, 30),
    "¿Qué es un 'for'?\n1. Bucle que ejecuta un bloque de código una determinada cantidad de veces\n2. Un bucle que se ejecuta mientras una condición sea verdadera\n3. Una sentencia que evalúa el valor de una variable en casos": (1, 25),
    "¿Qué es un 'enum'?\n1. Una clase que recibe los atributos y métodos de otra\n2. Una estructura que contiene campos y funciones\n3. Una colección de funciones que pueden ser implementadas en una clase\n4. Una colección de constantes enumeradas": (4, 20),
    "¿Qué es un callback?\n1. Un puntero a una función\n2. Una función que es pasada como argumento a otra función\n3. Una función que retorna un valor": (2, 30),
    "¿Cuál es la extensión de un archivo de código de Python?\n1. .rs\n2. .cpp\n3. .js\n4. .py": (4, 25),

}