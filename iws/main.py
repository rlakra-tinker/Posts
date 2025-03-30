#
# Author: Rohtash Lakra
#

# from starlette.responses import JSONResponse
from functools import lru_cache

from dotenv import (load_dotenv, find_dotenv)
from fastapi import FastAPI, Depends, status
from fastapi.responses import FileResponse, JSONResponse

from framework.orm.pydantic.model import ConfigSetting

# from globals import connector
# from rest.contact.mapper import ContactMapper
# from rest.contact.model import Contact
# from rest.contact.schema import ContactSchema
# from rest.contact.service import ContactService

load_dotenv(find_dotenv(".env"))

# Initialize 'FastAPI' Application
app = FastAPI(
    redirect_slashes=False,
    docs_url="/docs",
)

# print(ConfigSetting())
configSettings = ConfigSetting()
print(configSettings)


@lru_cache
def getSettings():
    return configSettings


# app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> JSONResponse:
    """Endpoint to prevent 404 when loading the docs"""
    return FileResponse("webapp/static/images/webapp-logo.png")
    # return JSONResponse(status_code=204, content="")


@app.get("/health-check", tags=["Basic Resources"], summary="Health Check", description="Returns Health Check Status")
async def healthCheck() -> JSONResponse:
    """The Health Check endpoint.
    Returns a default success message indicating the application is running.
    """
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "FastAPI ./v2/health-check"})


@app.get("/info", tags=["Basic Resources"], summary="Get Configs", description="Get '.env' Configs")
async def info(config: ConfigSetting = Depends(getSettings)):
    # return {
    #     "app_name": config.app_name,
    #     "admin_email": config.admin_email,
    #     "items": config.items,
    # }

    return config.model_dump()

#
# class ContactCreate(Contact):
#     pass
#
#
# @app.post("/contacts", response_model=Contact)
# def create_item(contact: Contact, session: Session = Depends(connector.getDatabase())):
#     contactService = ContactService()
#     contact = contactService.create(contact)
#     # contactSchema = ContactMapper.fromModel(contact)
#     # session.add(contactSchema)
#     # session.commit()
#     # session.refresh(contactSchema)
#     # return contactSchema
#     return contact
#
#
# @app.get("/contacts", response_model=List[Contact])
# def read_items(skip: int = 0, limit: int = 100, session: Session = Depends(connector.getDatabase())):
#     contactSchemas = session.query(ContactSchema).offset(skip).limit(limit).all()
#     contacts = ContactMapper.fromSchemas(contactSchemas)
#     return contacts
#
#
# @app.get("/contacts/{contact_id}", response_model=Contact)
# def read_item(contact_id: int, session: Session = Depends(connector.getDatabase())):
#     contactSchema = session.query(ContactSchema).filter(ContactSchema.id == contact_id).first()
#     if contactSchema is None:
#         raise HTTPException(status_code=404, detail="Record not found!")
#
#     contact = ContactMapper.fromSchema(contactSchema)
#     return contact
