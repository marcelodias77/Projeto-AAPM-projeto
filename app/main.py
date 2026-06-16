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
            <style>
                body {
                    background: #1a1a2e; 
                    color: white; 
                    height: 100vh; 
                    display: flex; 
                    flex-direction: column; 
                    justify-content: center; 
                    align-items: center; 
                    font-family: sans-serif;
                    text-align: center;
                    margin: 0;
                }
                h1 { font-size: 6rem; margin: 0; color: #e94560; }
                h2 { margin-top: 0; color: #fff; }
                p { color: #4e5166; max-width: 400px; padding: 0 20px; line-height: 1.6; }
                .btn {
                    margin-top: 20px; 
                    color: #e94560; 
                    text-decoration: none; 
                    border: 2px solid #e94560; 
                    padding: 10px 20px; 
                    border-radius: 5px;
                    font-weight: bold;
                    transition: all 0.3s;
                }
                .btn:hover { background: #e94560; color: white; }
            </style>
        </head>
        <body>
            <h1>404</h1>
            <h2>Caminho não foi encontrado</h2>
            <p>Desculpe, a rota que você tentou acessar não existe!</p>
            <a href="/" class="btn">Voltar para o Início</a>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=404)
