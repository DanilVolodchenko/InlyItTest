from ..exceptions import PermissionDenied
from ..models.dto.ad import CreateAd
from ..models.dto.common import AdDTO, UserDTO
from ..services import UserService, AdService

__all__ = ['AdController']


class AdController:

    def __init__(self, user_service: UserService, ad_service: AdService) -> None:
        self.user_service = user_service
        self.ad_service = ad_service

    def create_ad(self, ad: CreateAd, user_id: int) -> AdDTO:
        user = self.user_service.get_user_by_id(user_id)
        return self.ad_service.create_ad(ad, user.id)

    def get_all_ads(self) -> list[AdDTO]:
        return self.ad_service.get_ads()

    def get_by_id(self, ad_id: int) -> AdDTO:
        return self.ad_service.get_ad_by_id(ad_id)

    def delete_ad(self, ad_id: int, user: UserDTO) -> AdDTO:
        return self.ad_service.delete_ad(ad_id, owner=user)
