from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def auth():
    return {'message' : 'Voce accesou a rota padrão auth', "autenticado": False}