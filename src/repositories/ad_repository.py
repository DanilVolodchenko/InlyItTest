from typing import Optional

from sqlalchemy.orm import joinedload

from .interfaces import RepositoryInterface, T
from ..models.db.ad import Ad
from ..models.dto.ad import CreateAd

__all__ = ['AdRepository']


class AdRepository(RepositoryInterface[Ad]):

    def get_by_id(self, ident: int) -> Optional[Ad]:
        return self.query.options(
            joinedload(self.model.user),
        ).filter(self.model.id == ident).first()


    def create(self, ad: CreateAd, user_id: int) -> Ad:
        ad = Ad(**ad.model_dump(), user_id=user_id)
        self.session.add(ad)
        self.session.flush()

        return ad

    def delete(self, ad: Ad) -> Ad:
        self.session.delete(ad)
        self.session.flush()

        return ad
