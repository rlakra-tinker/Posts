#
# Author: Rohtash Lakra
#
import logging
from typing import List, Optional, Dict, Any

from framework.exception import DuplicateRecordException, ValidationException, NoRecordFoundException
from framework.http import HTTPStatus
from framework.orm.pydantic.model import AbstractModel
from framework.orm.sqlalchemy.schema import SchemaOperation
from framework.service import AbstractService
from rest.company.model import Company
from rest.company.repository import CompanyRepository
from rest.company.schema import CompanySchema

logger = logging.getLogger(__name__)


class CompanyService(AbstractService):

    def __init__(self):
        logger.debug("CompanyService()")
        self.repository = CompanyRepository()

    # @override
    def fromSchema(self, companySchema: CompanySchema) -> Company:
        return Company(**companySchema.toJSONObject())

    # @override
    def fromModel(self, company: Company) -> CompanySchema:
        return CompanySchema(**company.toJSONObject())

    def validate(self, operation: SchemaOperation, company: Company) -> None:
        logger.debug(f"+validate({operation}, {company})")
        # super().validate(operation, company)
        error_messages = []

        # validate the object
        if not company:
            error_messages.append("'Company' is not fully defined!")

        match operation.name:
            case SchemaOperation.CREATE.name:
                # validate the required fields
                if not company.name:
                    error_messages.append("Company 'name' is required!")

            case SchemaOperation.UPDATE.name:
                if not company.id:
                    error_messages.append("Company 'id' is required!")

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validate()")

    def findById(self, id: int) -> Company:
        return self.fromSchema(self.repository.findById(CompanySchema, id))

    # @override
    def findByFilter(self, filters: Dict[str, Any]) -> List[Optional[AbstractModel]]:
        logger.debug(f"+findByFilter({filters})")
        companySchemas = self.repository.findByFilter(filters)
        companyModels = []
        for companySchema in companySchemas:
            roleModel = self.fromSchema(companySchema)
            companyModels.append(roleModel)

        logger.debug(f"-findByFilter(), companyModels={companyModels}")
        return companyModels

    # @override
    def existsByFilter(self, filters: Dict[str, Any]) -> bool:
        """Returns True if the records exist by filter otherwise False"""
        logger.debug(f"+existsByFilter({filters})")
        companySchemas = self.repository.findByFilter(filters)
        result = True if companySchemas else False
        logger.debug(f"-existsByFilter(), result={result}")
        return result

    def validates(self, operation: SchemaOperation, roles: List[Company]) -> None:
        logger.debug(f"+validates({operation}, {roles})")
        error_messages = []

        # validate the object
        if not roles:
            error_messages.append('Roles is required!')

        for company in roles:
            self.validate(operation, company)

        # throw an error if any validation error
        if error_messages and len(error_messages) > 0:
            error = ValidationException(httpStatus=HTTPStatus.INVALID_DATA, messages=error_messages)
            logger.debug(f"{type(error)} = exception={error}")
            raise error

        logger.debug(f"-validates()")

    def create(self, company: Company) -> Company:
        """Crates a new company"""
        logger.debug(f"+create({company})")
        if self.existsByFilter({"name": company.name}):
            raise DuplicateRecordException(HTTPStatus.CONFLICT, f"[{company.name}] company already exists!")

        # company = self.repository.create(company)
        companySchema = self.fromModel(company)
        companySchema = self.repository.save(companySchema)
        if companySchema and companySchema.id is None:
            companySchema = self.repository.findByFilter({"name": company.name})

        company = self.fromSchema(companySchema)
        logger.debug(f"-create(), company={company}")
        return company

    def bulkCreate(self, roles: List[Company]) -> List[Company]:
        """Crates a new company"""
        logger.debug(f"+bulkCreate({roles})")
        results = []
        for company in roles:
            result = self.create(company)
            results.append(result)

        logger.debug(f"-bulkCreate(), results={results}")
        return results

    def update(self, company: Company) -> Company:
        """Updates the company"""
        logger.debug(f"+update({company})")
        # self.validate(SchemaOperation.UPDATE, company)
        # check record exists by id
        # if not self.existsByFilter({"id": company.id}):
        #     raise NoRecordFoundException(HTTPStatus.NOT_FOUND, f"Company doesn't exist!")
        companySchemas = self.repository.findByFilter({"id": company.id})
        companySchema = companySchemas[0]
        if company.name and companySchema.name != company.name:
            companySchema.name = company.name

        if company.active and companySchema.active != company.active:
            companySchema.active = company.active

        if company.meta_data and companySchema.meta_data != company.meta_data:
            companySchema.meta_data = company.meta_data

        # companySchema = self.fromModel(oldRole)
        self.repository.update(companySchema)
        # companySchema = self.repository.update(mapper=CompanySchema, mappings=[companySchema])
        companySchema = self.repository.findByFilter({"id": company.id})[0]
        company = self.fromSchema(companySchema)
        logger.debug(f"-update(), company={company}")
        return company

    def delete(self, id: int) -> None:
        logger.debug(f"+delete({id})")
        # check record exists by id
        if self.existsByFilter({"id": id}):
            self.repository.delete(id)
        else:
            raise NoRecordFoundException(HTTPStatus.NOT_FOUND, "Company doesn't exist!")

        logger.debug(f"-delete()")
