from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.controllers import auth_controller
from app.controllers import admin_controller
from app.controllers import categoria_controller
from app.controllers import produto_controller
from app.controllers import movimentacao_controller
from app.controllers import cliente_controller
from app.controllers import pdv_controller

from app.auth import get_usuario_opcional

app = FastAPI(title="Sistema AAPM")

#Configurar o fastapi para servir os arquivos CSS, JS, IMG
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#Configura para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")


# Inclui os routeres do controller
app.include_router(auth_controller.router)
app.include_router(admin_controller.router)
app.include_router(categoria_controller.router)
app.include_router(produto_controller.router)
app.include_router(movimentacao_controller.router)
app.include_router(cliente_controller.router)
app.include_router(pdv_controller.router)


@app.get("/")
def tela_home(
    request: Request, 
    usuario = Depends(get_usuario_opcional)
    ):

    #Não logado - exibe a tela index
    if usuario is None:
        return templates.TemplateResponse(
            request,
            "index.html",
            {"request": request}
        )
    # Logado - exibe a tela home
    return templates.TemplateResponse(
            request,
            "home.html",
            {"request": request, "usuario": usuario}
        )

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        html_content = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>404 — ERROR</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
            
            <style>
                :root {
                    --bg-base: #000000;       /* Preto absoluto idêntico à imagem */
                    --glitch-red: #e61c1c;    /* Vermelho puro e denso da referência */
                    --text-main: #ffffff;
                    --text-muted: #64748b;
                    --radius-md: 12px;
                    --transition: all 0.3s ease;
                }

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                body {
                    background-color: var(--bg-base);
                    color: var(--text-main);
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    font-family: 'Inter', sans-serif;
                    text-align: center;
                    overflow: hidden;
                    -webkit-font-smoothing: antialiased;
                }

                .error-container {
                    padding: 0 24px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                /* --- EFEITO GLITCH ALINHADO COM A IMAGEM --- */
                .glitch-wrapper {
                    font-family: 'Share Tech Mono', monospace;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 40px;
                    user-select: none;
                }

                /* Texto ERROR: Branco, largo, exatamente acima do 404 */
                .glitch-text {
                    font-size: 4rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 14px;
                    color: #ffffff;
                    line-height: 0.9;
                    margin-bottom: 5px;
                    padding-left: 14px; /* Compensa o letter-spacing para manter perfeitamente centralizado */
                    position: relative;
                    animation: textGlowPulse 2s infinite alternate;
                }

                /* Número 404: Vermelho e gigante */
                .glitch-number {
                    font-size: 11rem;
                    font-weight: 700;
                    line-height: 0.85;
                    color: var(--glitch-red);
                    letter-spacing: -2px;
                    position: relative;
                }

                /* Pseudo-elementos para criar os cortes horizontais da imagem */
                .glitch-number::before, .glitch-number::after,
                .glitch-text::before, .glitch-text::after {
                    content: attr(data-text);
                    position: absolute;
                    left: 0;
                    top: 0;
                    width: 100%;
                    height: 100%;
                    background: var(--bg-base);
                }

                /* Configuração do espaçamento dos cortes horizontais */
                .glitch-text::before, .glitch-number::before {
                    clip: rect(15px, 9999px, 22px, 0);
                    animation: glitch-slice-1 2.5s infinite linear alternate-reverse;
                }

                .glitch-text::after, .glitch-number::after {
                    clip: rect(60px, 9999px, 68px, 0);
                    animation: glitch-slice-2 2s infinite linear alternate-reverse;
                }

                /* Elementos adicionais para simular os blocos vazados da imagem */
                .glitch-number::before {
                    color: var(--glitch-red);
                }
                .glitch-text::before {
                    color: #ffffff;
                }

                h2 {
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: 10px;
                    letter-spacing: -0.5px;
                }

                p {
                    color: var(--text-muted);
                    font-size: 0.95rem;
                    max-width: 400px;
                    margin: 0 auto 36px auto;
                    line-height: 1.6;
                }

                /* Botão Customizado */
                .btn {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    color: #ffffff;
                    background-color: transparent;
                    border: 2px solid var(--glitch-red);
                    text-decoration: none;
                    padding: 12px 28px;
                    border-radius: var(--radius-md);
                    font-size: 0.95rem;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                    transition: var(--transition);
                }

                .btn:hover {
                    background-color: var(--glitch-red);
                    box-shadow: 0 0 25px rgba(230, 28, 28, 0.5);
                    transform: translateY(-2px);
                }

                .btn:active {
                    transform: translateY(0);
                }

                /* --- KEYFRAMES DO CORTE DIGITAL (IDÊNTICO À IMAGEM) --- */
                @keyframes glitch-slice-1 {
                    0% { clip: rect(20px, 9999px, 25px, 0); transform: translateX(-4px); text-shadow: 2px 0 0 calc(var(--glitch-red)); }
                    20% { clip: rect(50px, 9999px, 54px, 0); transform: translateX(3px); }
                    40% { clip: rect(10px, 9999px, 14px, 0); transform: translateX(-2px); }
                    60% { clip: rect(85px, 9999px, 92px, 0); transform: translateX(4px); }
                    80% { clip: rect(35px, 9999px, 39px, 0); transform: translateX(-3px); }
                    100% { clip: rect(62px, 9999px, 68px, 0); transform: translateX(2px); }
                }

                @keyframes glitch-slice-2 {
                    0% { clip: rect(70px, 9999px, 76px, 0); transform: translateX(4px); }
                    25% { clip: rect(5px, 9999px, 12px, 0); transform: translateX(-3px); }
                    50% { clip: rect(110px, 9999px, 116px, 0); transform: translateX(2px); }
                    75% { clip: rect(45px, 9999px, 51px, 0); transform: translateX(-4px); }
                    100% { clip: rect(90px, 9999px, 95px, 0); transform: translateX(3px); }
                }

                @keyframes textGlowPulse {
                    from { text-shadow: 0 0 2px rgba(255,255,255,0.1); }
                    to { text-shadow: 0 0 8px rgba(255,255,255,0.3); }
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                <div class="glitch-wrapper">
                    <div class="glitch-text" data-text="ERROR">ERROR</div>
                    <div class="glitch-number" data-text="404">404</div>
                </div>

                <h2>Caminho não encontrado</h2>
                <p>A rota que você tentou acessar não existe no sistema AAPM.</p>
                
                <a href="/" class="btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                    Voltar para o Início
                </a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=404)
    
@app.exception_handler(403)
async def custom_403_handler(request: Request, exc: StarletteHTTPException):
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>403 — ACCESS DENIED</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
        
        <style>
            :root {
                --bg-base: #000000;       /* Preto absoluto */
                --glitch-red: #e61c1c;    /* Vermelho puro */
                --text-main: 1ffffff;
                --text-muted: #64748b;
                --radius-md: 12px;
                --transition: all 0.3s ease;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                background-color: var(--bg-base);
                color: var(--text-main);
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: 'Inter', sans-serif;
                text-align: center;
                overflow: hidden;
            }

            .error-container { padding: 0 24px; display: flex; flex-direction: column; align-items: center; }

            .glitch-wrapper {
                font-family: 'Share Tech Mono', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-bottom: 40px;
                user-select: none;
            }

            .glitch-text {
                font-size: 4rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 14px;
                color: #ffffff;
                line-height: 0.9;
                margin-bottom: 5px;
                padding-left: 14px;
                position: relative;
            }

            .glitch-number {
                font-size: 11rem;
                font-weight: 700;
                line-height: 0.85;
                color: var(--glitch-red);
                letter-spacing: -2px;
                position: relative;
            }

            .glitch-number::before, .glitch-number::after,
            .glitch-text::before, .glitch-text::after {
                content: attr(data-text);
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background: var(--bg-base);
            }

            .glitch-text::before, .glitch-number::before {
                clip: rect(15px, 9999px, 22px, 0);
                animation: glitch-slice-1 2.5s infinite linear alternate-reverse;
                color: var(--glitch-red);
            }

            .glitch-text::after, .glitch-number::after {
                clip: rect(60px, 9999px, 68px, 0);
                animation: glitch-slice-2 2s infinite linear alternate-reverse;
                color: #ffffff;
            }

            h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; letter-spacing: -0.5px; }
            p { color: var(--text-muted); font-size: 0.95rem; max-width: 400px; margin: 0 auto 36px auto; line-height: 1.6; }

            .btn {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                color: #ffffff;
                background-color: transparent;
                border: 2px solid var(--glitch-red);
                text-decoration: none;
                padding: 12px 28px;
                border-radius: var(--radius-md);
                font-size: 0.95rem;
                font-weight: 600;
                transition: var(--transition);
            }

            .btn:hover {
                background-color: var(--glitch-red);
                box-shadow: 0 0 25px rgba(230, 28, 28, 0.5);
                transform: translateY(-2px);
            }

            @keyframes glitch-slice-1 {
                0% { clip: rect(20px, 9999px, 25px, 0); transform: translateX(-4px); }
                40% { clip: rect(10px, 9999px, 14px, 0); transform: translateX(-2px); }
                100% { clip: rect(62px, 9999px, 68px, 0); transform: translateX(2px); }
            }

            @keyframes glitch-slice-2 {
                0% { clip: rect(70px, 9999px, 76px, 0); transform: translateX(4px); }
                50% { clip: rect(110px, 9999px, 116px, 0); transform: translateX(2px); }
                100% { clip: rect(90px, 9999px, 95px, 0); transform: translateX(3px); }
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="glitch-wrapper">
                <div class="glitch-text" data-text="PROIBIDO">PROIBIDO</div>
                <div class="glitch-number" data-text="403">403</div>
            </div>

            <h2>Acesso Restrito</h2>
            <p>Seu perfil de operador não possui permissões para acessar esta pagina!</p>
            
            <a href="/" class="btn">Voltar para o Início</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=403)


# --- MANIPULADOR GENÉRICO (EVITA QUE QUALQUER OUTRA QUEBRA MOSTRE A TELA BRANCA) ---
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # Se for 404, executa a lógica do seu manipulador 404 já existente
        return await custom_404_handler(request, exc)
    elif exc.status_code == 403:
        return await custom_403_handler(request, exc)
    
    # Caso aconteça um erro 500 real por bug no código, não mostra a página em branco pura:
    return HTMLResponse(content=f"<h1>Erro {exc.status_code}</h1><p>{exc.detail}</p>", status_code=exc.status_code)