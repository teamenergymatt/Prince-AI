from flask import Flask, request, render_template_string, session
from openai import OpenAI
import os

app = Flask(__name__)

app.secret_key = "prince-ai-secret-key"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

MODELO = "gpt-5.6-luna"

INSTRUCCIONES = """
Eres Prince AI, un asistente de inteligencia artificial generalista.

Tu nombre es Prince AI.

Puedes hablar de:
- ciencia
- historia
- tecnología
- programación
- matemáticas
- economía
- deporte
- fútbol
- videojuegos
- estudios
- negocios
- cultura
- escritura
- ideas
- creatividad
- resúmenes
- planificación
- prácticamente cualquier tema general

Normas:
- Responde en español salvo que el usuario escriba claramente en otro idioma.
- Sé claro, natural e inteligente.
- No inventes datos actuales.
- Si una pregunta depende de información reciente, usa búsqueda web.
- No digas que eres ChatGPT.
- Si te preguntan qué tecnología utilizas, explica que Prince AI usa modelos de OpenAI mediante API.
- Mantén el contexto de la conversación.
- Adapta la longitud de la respuesta a lo que pida el usuario.
"""

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Prince AI</title>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #050505;
    color: white;
}

.container {
    max-width: 900px;
    margin: auto;
    padding: 20px;
}

.logo {
    text-align: center;
    margin-bottom: 20px;
}

.logo img {
    width: 150px;
    border-radius: 20px;
}

.logo h1 {
    font-family: Georgia, serif;
    letter-spacing: 8px;
    font-size: 34px;
    margin-bottom: 5px;
}

.logo p {
    color: #d4af67;
    letter-spacing: 3px;
    font-size: 12px;
}

.chat {
    background: #101010;
    border: 1px solid #242424;
    border-radius: 20px;
    padding: 20px;
    min-height: 450px;
}

.mensaje {
    margin-bottom: 20px;
}

.usuario {
    text-align: right;
}

.usuario span {
    display: inline-block;
    background: #d4af67;
    color: black;
    padding: 12px 16px;
    border-radius: 16px;
    max-width: 75%;
}

.ia span {
    display: inline-block;
    background: #1b1b1b;
    padding: 12px 16px;
    border-radius: 16px;
    max-width: 75%;
    white-space: pre-wrap;
}

form {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}

textarea {
    flex: 1;
    padding: 15px;
    background: #111;
    color: white;
    border: 1px solid #333;
    border-radius: 15px;
    font-size: 16px;
    resize: none;
}

button {
    background: #d4af67;
    border: none;
    border-radius: 15px;
    padding: 0 20px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #f0cf87;
}

.nuevo {
    margin-top: 10px;
    text-align: right;
}

.nuevo a {
    color: #d4af67;
    text-decoration: none;
}

</style>

</head>

<body>

<div class="container">

<div class="logo">

<img src="/static/prince_logo.png">

<h1>PRINCE AI</h1>

<p>INTELLIGENCE FOR A BRIGHTER TOMORROW</p>

</div>

<div class="chat">

{% if not historial %}

<div style="text-align:center; padding-top:100px; color:#aaa">

<h2>¿En qué puedo ayudarte?</h2>

<p>
Pregunta sobre ciencia, tecnología, programación, historia,
fútbol, negocios, estudios o cualquier otro tema.
</p>

</div>

{% endif %}

{% for mensaje in historial %}

{% if mensaje["role"] == "user" %}

<div class="mensaje usuario">
<span>{{ mensaje["content"] }}</span>
</div>

{% else %}

<div class="mensaje ia">
<span>{{ mensaje["content"] }}</span>
</div>

{% endif %}

{% endfor %}

</div>

<form method="POST">

<textarea
name="mensaje"
rows="3"
placeholder="Escribe un mensaje..."
required
></textarea>

<button type="submit">
Enviar
</button>

</form>

<div class="nuevo">
<a href="/nuevo">Nueva conversación</a>
</div>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def inicio():

    if "historial" not in session:
        session["historial"] = []

    historial = session["historial"]

    if request.method == "POST":

        mensaje = request.form.get("mensaje", "").strip()

        if mensaje:

            historial.append({
                "role": "user",
                "content": mensaje
            })

            try:

                mensajes_openai = []

                for item in historial:

                    mensajes_openai.append({
                        "role": item["role"],
                        "content": item["content"]
                    })

                respuesta = client.responses.create(
                    model=MODELO,
                    instructions=INSTRUCCIONES,
                    input=mensajes_openai,
                    tools=[
                        {
                            "type": "web_search"
                        }
                    ]
                )

                texto = respuesta.output_text

            except Exception as error:

                print("ERROR:", error)

                texto = (
                    "Ha ocurrido un error al conectar con Prince AI. "
                    "Revisa la ventana de PowerShell."
                )

            historial.append({
                "role": "assistant",
                "content": texto
            })

            session["historial"] = historial

    return render_template_string(
        HTML,
        historial=historial
    )


@app.route("/nuevo")
def nuevo_chat():

    session["historial"] = []

    return """
    <script>
    window.location.href = "/";
    </script>
    """


if __name__ == "__main__":

    print("")
    print("==============================")
    print("        PRINCE AI")
    print("==============================")
    print("")
    print("Servidor arrancado.")
    print("Abre: http://127.0.0.1:5000")
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )