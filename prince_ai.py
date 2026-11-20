from flask import Flask, request, render_template_string, session, jsonify
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
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f6f7fb">
<title>Prince AI</title>
<style>
:root{color-scheme:light;--ink:#171b2b;--muted:#525a71;--line:#dfe3ee;--accent:#353ca7;--surface:#fff;--canvas:#f6f7fb;font:16px/1.6 system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink)}button,textarea{font:inherit}a{color:inherit}header{border-bottom:1px solid var(--line);background:var(--surface)}.bar{max-width:1100px;margin:auto;padding:14px 24px;display:flex;justify-content:space-between;align-items:center;gap:16px}.brand{display:inline-flex;gap:10px;align-items:center;font-weight:800;text-decoration:none;letter-spacing:-.03em}.mark{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:11px;background:#232858;color:#d7ddff;font-size:21px;font-weight:850;line-height:1;letter-spacing:-.06em}.mark.hero-mark{width:63px;height:63px;border-radius:20px;font-size:40px;box-shadow:0 12px 26px #23285824}.reset{font-size:.88rem;text-decoration:none;padding:6px 10px;border:1px solid var(--line);border-radius:8px}.reset:hover,.prompt:hover{border-color:#8d92c3;background:#f0f1ff}main{width:min(100% - 32px,780px);margin:auto}.empty{padding:clamp(32px,10vh,105px) 0 28px;text-align:center}.empty h1{font-size:clamp(2rem,6vw,3.65rem);line-height:1.12;letter-spacing:-.055em;margin:.45em 0 .2em}.empty p{color:var(--muted);margin:0}.prompts{display:flex;flex-wrap:wrap;justify-content:center;gap:9px;margin:24px 0 0}.prompt{color:var(--ink);border:1px solid var(--line);background:white;border-radius:999px;padding:8px 13px;cursor:pointer;font-size:.88rem}.messages{display:grid;gap:18px;padding:29px 0 25px}.message{max-width:100%;min-width:0}.message.user{justify-self:end;max-width:85%;border-radius:15px 15px 3px 15px;background:#e8ebff;padding:10px 15px}.message.assistant{border:1px solid var(--line);background:white;border-radius:15px;padding:13px 16px}.message b{display:block;color:var(--muted);font-size:.78rem;margin-bottom:3px}.message p{white-space:pre-wrap;overflow-wrap:anywhere;margin:0}.compose-panel{position:sticky;bottom:0;background:var(--canvas);padding:10px 0 max(10px,env(safe-area-inset-bottom))}.composer{border:1px solid var(--line);box-shadow:0 6px 20px #2328580d;background:white;border-radius:16px;padding:10px;display:flex;align-items:end;gap:10px}textarea{border:0;min-width:0;flex:1;resize:vertical;min-height:48px;max-height:180px;background:white;color:var(--ink);padding:8px}.send{border:0;border-radius:10px;background:var(--accent);color:white;padding:10px 14px;cursor:pointer;font-weight:700}.send:disabled{opacity:.65}.hint{font-size:.78rem;color:var(--muted);text-align:center;margin:7px 0 0}a:focus-visible,button:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:3px}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}@media(max-width:480px){.bar{padding-inline:16px}.empty{padding-top:40px}.prompts{gap:7px}.prompt{padding:6px 10px}.composer{gap:5px}.send{padding-inline:10px}}
</style>
</head>
<body>
<header><div class="bar"><a class="brand" href="/"><span class="mark" aria-hidden="true">P</span>Prince AI</a>{% if historial %}<a class="reset" href="/nuevo">Nueva conversación</a>{% endif %}</div></header>
<main>
{% if not historial %}
<section class="empty">
<span class="mark hero-mark" aria-hidden="true">P</span>
<h1>¿En qué puedo ayudarte?</h1>
<p>Pregunta, aprende o empieza a darle forma a una idea.</p>
<div class="prompts" aria-label="Ideas para empezar">
<button type="button" class="prompt" data-prompt="Hola, Prince. ¿Para qué fuiste creado y en qué puedes ayudarme?">Conoce a Prince</button>
<button type="button" class="prompt" data-prompt="Ayúdame a crear una ruta de aprendizaje. Primero pregúntame qué quiero aprender, mi nivel y cuánto tiempo tengo.">Crea una ruta</button>
<button type="button" class="prompt" data-prompt="Ayúdame a explorar una idea. Pregúntame qué tengo en mente y proponme opciones concretas.">Explora una idea</button>
</div>
</section>
{% else %}
<section class="messages" aria-label="Conversación">
{% for mensaje in historial %}
<article class="message {{ 'user' if mensaje['role'] == 'user' else 'assistant' }}">
<b>{{ 'Tú' if mensaje['role'] == 'user' else 'Prince AI' }}</b><p>{{ mensaje['content'] }}</p>
</article>
{% endfor %}
</section>
{% endif %}
<div class="compose-panel">
<form method="post" class="composer" id="composer">
<label class="sr-only" for="mensaje">Mensaje para Prince</label>
<textarea id="mensaje" name="mensaje" rows="2" placeholder="Escribe a Prince…" required></textarea>
<button class="send" type="submit">Enviar</button>
</form>
<p class="hint" id="status" role="status">Prince puede cometer errores. Comprueba la información importante.</p>
</div>
</main>
<script>
const composer=document.querySelector('#composer');
const message=document.querySelector('#mensaje');
for(const btn of document.querySelectorAll('.prompt')){
  btn.addEventListener('click',()=>{message.value=btn.dataset.prompt;message.focus();});
}
composer.addEventListener('submit',()=>{
  const button=composer.querySelector('.send');
  button.disabled=true;
  button.textContent='Enviando…';
  document.querySelector('#status').textContent='Prince está preparando tu respuesta…';
});
addEventListener('pageshow',event=>{
  if(event.persisted){
    const button=composer.querySelector('.send');
    button.disabled=false;
    button.textContent='Enviar';
    document.querySelector('#status').textContent='Prince puede cometer errores. Comprueba la información importante.';
  }
});
if(document.querySelector('.messages'))window.scrollTo(0,document.body.scrollHeight);
</script>
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




# CONEXIÓN DE PRINCE AI CON FOUNDY
import time
import json
from collections import defaultdict, deque
from threading import Lock

_foundy_requests = defaultdict(deque)
_foundy_lock = Lock()

@app.after_request
def foundy_cors(response):
    origin = request.headers.get("Origin")
    allowed = {"null"}  # Prototipo HTML abierto como archivo
    public_origin = os.environ.get("FOUNDY_ORIGIN", "").rstrip("/")
    if public_origin:
        allowed.add(public_origin)

    if request.path == "/api/chat" and origin in allowed:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/api/chat", methods=["POST", "OPTIONS"])
def foundy_chat():
    if request.method == "OPTIONS":
        return "", 204

    if os.environ.get("FOUNDY_API_ENABLED") != "true":
        return jsonify(error="API no activada"), 503

    origin = request.headers.get("Origin")
    valid_origins = {"null"}
    public_origin = os.environ.get("FOUNDY_ORIGIN", "").rstrip("/")
    if public_origin:
        valid_origins.add(public_origin)

    if origin not in valid_origins:
        return jsonify(error="Origen no autorizado"), 403

    ip = request.remote_addr or "unknown"
    now = time.time()

    with _foundy_lock:
        history = _foundy_requests[ip]
        while history and now - history[0] > 3600:
            history.popleft()
        if len(history) >= 15:
            return jsonify(error="Límite de uso alcanzado"), 429
        history.append(now)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="JSON inválido"), 400

    message = data.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return jsonify(error="Mensaje vacío"), 400
    message = message.strip()[:1500]

    context = data.get("context", {})
    if not isinstance(context, (dict, list)):
        context = {}
    project = json.dumps(context, ensure_ascii=False)[:3000]

    instructions = (


    "Eres Prince AI, el asistente inteligente de CartaQR. "
    "Ayudas a diseñar cartas digitales profesionales. "
    "Eres experto en restaurantes y hostelería. "
    "No inventes precios ni información sobre alérgenos. "
    "Responde en español de forma clara y profesional."
    )

    try:

        result = client.responses.create(
            model=MODELO,
            instructions=instructions,
            input=(
                "Contexto del proyecto:\n" + project +
                "\n\nPregunta del emprendedor:\n" + message
            ),
            max_output_tokens=450
        )
        return jsonify(reply=result.output_text)
    except Exception:
        app.logger.exception("Error en FOUNDY")
        return jsonify(error="Prince AI no pudo responder"), 502

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
