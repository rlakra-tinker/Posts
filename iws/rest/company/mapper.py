#
# Author: Rohtash Lakra
#
from framework.orm.mapper import Mapper
from rest.company.model import Company
from rest.company.schema import CompanySchema


class CompanyMapper(Mapper):

    @classmethod
    # @override
    def fromSchema(self, companySchema: CompanySchema) -> Company:
        return Company(**companySchema.toJSONObject())

    @classmethod
    # @override
    def fromModel(self, company: Company) -> CompanySchema:
        return CompanySchema(**company.toJSONObject())
