from sqlalchemy import select
from sqlalchemy.orm import aliased

from infrastructure.database.models import AuthorDescriptionModel, AuthorModel, SequenceDescriptionModel, SequenceModel
from infrastructure.database.repo.base import BaseRepo
from infrastructure.dtos.sequence_dtos import SequenceDTO, SequenceInfoDTO


class SequencesRepo(BaseRepo):
    async def get_sequence_by_book_id(self, book_id: int) -> list[SequenceInfoDTO] | None:
        query = (
            select(SequenceDescriptionModel, SequenceModel)
            .join(SequenceModel, SequenceDescriptionModel.seq_id == SequenceModel.seq_id)
            .where(SequenceDescriptionModel.book_id == book_id)
        )
        result = await self.session.execute(query)
        sequences = result.all()

        if not sequences:
            return []
        return [
            SequenceInfoDTO(seq_name=sequence.seq_name, **description.__dict__) for description, sequence in sequences
        ]

    async def get_sequences_by_name(self, seq_name: str) -> list[SequenceDTO] | None:
        SequenceAlias = aliased(SequenceModel)
        AuthorAlias = aliased(AuthorModel)
        AuthorDescriptionAlias = aliased(AuthorDescriptionModel)

        query = (
            select(
                SequenceAlias.seq_id,
                SequenceAlias.seq_name,
                AuthorDescriptionAlias.first_name,
                AuthorDescriptionAlias.middle_name,
                AuthorDescriptionAlias.last_name,
            )
            .join(SequenceDescriptionModel, SequenceDescriptionModel.seq_id == SequenceAlias.seq_id)
            .join(AuthorAlias, AuthorAlias.book_id == SequenceDescriptionModel.book_id)
            .join(AuthorDescriptionAlias, AuthorDescriptionAlias.author_id == AuthorAlias.author_id)
            .filter(SequenceAlias.seq_name.like(f"%{seq_name}%")).distinct()
        )

        result = await self.session.execute(query)
        sequences = result.all()

        if not sequences:
            return []

        return [SequenceDTO(
            seq_id=sequence.seq_id,
            seq_name=sequence.seq_name,
            seq_author_name=f'{sequence.first_name} {sequence.middle_name} {sequence.last_name}'
        ) for sequence in sequences]
