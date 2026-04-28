"""
Routes para escolas
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas
from app.models import obter_sessao
from app.services.escolas_service import EscolasService

router = APIRouter()

@router.get("/")
async def listar_escolas(
    ano: int = Query(None, description="Filtrar por ano"),
    estado_id: int = Query(None, description="Filtrar por estado"),
    rede: str = Query(None, description="Filtrar por rede (Pública/Privada)"),
    db: Session = Depends(obter_sessao)
):
    """Lista todas as escolas com filtros opcionais"""
    try:
        escolas = EscolasService.obter_todas(db, ano, estado_id, rede)
        return {
            "sucesso": True,
            "total": len(escolas),
            "dados": escolas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{escola_id}")
async def obter_escola(escola_id: int, db: Session = Depends(obter_sessao)):
    """Obtém escola específica"""
    escola = EscolasService.obter_por_id(db, escola_id)
    if not escola:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    return {"sucesso": True, "dado": escola}

@router.get("/total/nacional")
async def obter_total_nacional(
    ano: int = Query(None, description="Filtrar por ano"),
    db: Session = Depends(obter_sessao)
):
    """Obtém total nacional de escolas"""
    total = EscolasService.obter_total_nacional(db, ano)
    return {"sucesso": True, "total": int(total)}

@router.get("/por-rede/")
async def obter_por_rede(
    ano: int = Query(..., description="Ano obrigatório"),
    db: Session = Depends(obter_sessao)
):
    """Agrupa escolas por rede"""
    try:
        dados = EscolasService.obter_por_rede(db, ano)
        resultado = [
            {
                "rede": d[0],
                "total_escolas": int(d[1] or 0),
                "total_matriculas": int(d[2] or 0)
            }
            for d in dados
        ]
        return {"sucesso": True, "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/por-localizacao/")
async def obter_por_localizacao(
    ano: int = Query(..., description="Ano obrigatório"),
    db: Session = Depends(obter_sessao)
):
    """Agrupa escolas por localização"""
    try:
        dados = EscolasService.obter_por_localizacao(db, ano)
        resultado = [
            {
                "localizacao": d[0],
                "total_escolas": int(d[1] or 0),
                "total_matriculas": int(d[2] or 0)
            }
            for d in dados
        ]
        return {"sucesso": True, "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/por-estado/")
async def obter_por_estado(
    ano: int = Query(..., description="Ano obrigatório"),
    db: Session = Depends(obter_sessao)
):
    """Agrupa escolas por estado"""
    try:
        dados = EscolasService.obter_por_estado(db, ano)
        resultado = [
            {
                "estado": d[1],
                "nome": d[0],
                "total_escolas": int(d[2] or 0),
                "total_matriculas": int(d[3] or 0)
            }
            for d in dados
        ]
        return {"sucesso": True, "total": len(resultado), "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historico/evolucao")
async def obter_evolucao(db: Session = Depends(obter_sessao)):
    """Obtém evolução histórica de escolas"""
    try:
        dados = EscolasService.obter_evolucao_historica(db)
        resultado = [
            {
                "ano": int(d[0]),
                "total_escolas": int(d[1] or 0),
                "escolas_publicas": int(d[2] or 0),
                "escolas_privadas": int(d[3] or 0),
                "escolas_rurais": int(d[4] or 0)
            }
            for d in dados
        ]
        return {"sucesso": True, "dados": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def criar_escola(
    escola: schemas.EscolaCreate,
    db: Session = Depends(obter_sessao)
):
    """Cria nova escola"""
    try:
        nova_escola = EscolasService.criar(db, escola)
        return {"sucesso": True, "mensagem": "Escola criada com sucesso", "id": nova_escola.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
