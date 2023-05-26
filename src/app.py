from pathlib import Path

from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

from src.utils.logger import CustomizeLogger
from src.exceptions.user import UserException
from src.exceptions.project import ProjectException
from src.exceptions.authentication import AuthenticationException
from src.views.user import router as user_router
from src.views.project import router as project_router
from src.views.view import router as view_router


def create_app(config_path: Path = Path("src/configs/logging_config.json")) -> FastAPI:
    CustomizeLogger.make_logger(config_path)

    app = FastAPI(title="Prefab project", debug=False)
    app.secret_key = "BAD_SECRET_KEY"

    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(ProjectException)
    async def project_exception_handler(request: Request, exc: ProjectException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"success": False, "message": str(exc)},
        )

    @app.get(
        "/",
        response_class=JSONResponse,
        status_code=status.HTTP_200_OK,
        description="Service health check request",
    )
    async def healthcheck_endpoint(response: Response):
        try:
            pass
        except Exception:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"success": False}
        else:
            return {"success": True}

    app.include_router(
        user_router,
        prefix="/user",
        tags=["User"],
    )

    app.include_router(
        project_router,
        prefix="/project",
        tags=["Project"],
    )

    app.include_router(
        view_router,
        tags=["Utils"],
    )

    return app
