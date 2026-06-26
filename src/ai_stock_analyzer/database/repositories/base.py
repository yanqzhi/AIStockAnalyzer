"""Base repository contracts."""

from typing import Protocol, TypeVar

Entity = TypeVar("Entity")
EntityId = TypeVar("EntityId")


class Repository(Protocol[Entity, EntityId]):
    """Protocol for persistence repositories."""

    def create(self, entity: Entity) -> EntityId:
        """Persist an entity.

        Args:
            entity: Entity to persist.

        Returns:
            Identifier for the persisted entity.
        """

    def get(self, entity_id: EntityId) -> Entity | None:
        """Fetch an entity by identifier.

        Args:
            entity_id: Entity identifier.

        Returns:
            The entity when found, otherwise None.
        """

    def list_all(self) -> list[Entity]:
        """Fetch all entities.

        Returns:
            List of persisted entities.
        """

    def update(self, entity_id: EntityId, entity: Entity) -> None:
        """Update an existing entity.

        Args:
            entity_id: Entity identifier.
            entity: Replacement entity data.
        """

    def delete(self, entity_id: EntityId) -> None:
        """Delete an entity by identifier.

        Args:
            entity_id: Entity identifier.
        """
