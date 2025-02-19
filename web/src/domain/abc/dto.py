from pydantic import BaseModel, ConfigDict, Field


class ABCDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        arbitrary_types_allowed=True
    )


class ABCResponse(ABCDTO):
    pass


class PaginationDTO(ABCDTO):
    page: int = Field(1, ge=1, description='Номер текущей страницы')
    page_size: int = Field(10, ge=1, le=100, description='Количесalembic.iniтво элементов на страницу')


class PaginationInfoDTO(ABCDTO):
    page: int = Field(0, ge=0, description='Номер текущей страницы')
    page_size: int = Field(10, ge=1, le=100, description='Количество элементов на страницу')
    page_count: int = Field(0, ge=0, description='Общее количество страниц.')
    total: int = Field(0, ge=0, description='Общее количество элементов.')
