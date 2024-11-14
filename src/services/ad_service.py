from typing import Type

from sqlalchemy.orm import Session

from .interfaces import ServiceInterface
from ..repositories import AdRepository
from ..models.dto.common import AdDTO, UserDTO
from ..models.dto.ad import CreateAd
from ..exceptions import AdNotFound, PermissionDenied

__all__ = ['AdService']


class AdService(ServiceInterface[AdRepository]):

    def __init__(self, session: Session, repository: Type[AdRepository] = AdRepository):
        super().__init__(session, repository)

    def get_ad_by_id(self, ad_id: int) -> AdDTO:
        ad = self.repository.get_by_id(ad_id)
        if not ad:
            raise AdNotFound('Статья не найдена')

        return AdDTO.model_validate(ad)

    def get_ads(self) -> list[AdDTO]:
        ads = self.repository.get_all()

        return [AdDTO.model_validate(ad) for ad in ads]

    def create_ad(self, ad: CreateAd, user_id: int) -> AdDTO:
        ad = self.repository.create(ad, user_id)

        return AdDTO.model_validate(ad)

    def delete_ad(self, ad_id: int, owner: UserDTO) -> AdDTO:
        ad = self.repository.get_by_id(ad_id)
        if not ad:
            raise AdNotFound('Статья не найдена')

        if ad.user.id != owner.id:
            raise PermissionDenied('Нельзя удалить не свою статью')

        deleted_ad = self.repository.delete(ad)

        return AdDTO.model_validate(deleted_ad)