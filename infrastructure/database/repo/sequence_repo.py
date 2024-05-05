from typing import Optional, List

from sqlalchemy import select

from infrastructure.database.models import SequenceModel, SequenceDescriptionModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.sequence_dtos import SequenceInfoDTO


class SequenceRepo(BaseRepo):
    async def get_sequences_by_book_id(self, book_id: int) -> Optional[List[SequenceInfoDTO]]:
        query = (
            select(SequenceDescriptionModel, SequenceModel)
            .join(SequenceModel, SequenceDescriptionModel.seq_id == SequenceModel.seq_id)
            .where(SequenceDescriptionModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        sequences = result.all()

        if not sequences:
            return []
        return [SequenceInfoDTO(
            seq_name=sequence.seq_name,
            **description.__dict__
        ) for description, sequence in sequences]
