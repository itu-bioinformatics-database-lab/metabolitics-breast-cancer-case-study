from .base_resource import BaseResource
from ..tasks import add_together


class StartWithQuery(BaseResource):

    def get(self, query):
        add_together.delay(23, 42)
        return [
            i.name
            for i in self._model.metabolites
            if i.name.startswith(query)
        ]


class SearchQuery(BaseResource):
    pass


class MetaboliteDetails(BaseResource):
    pass


class ReactionDetails(BaseResource):
    pass


class RelatedReaction(BaseResource):
    pass


class RelatedMetabolites(BaseResource):
    pass


class SubsystemDetails(BaseResource):
    pass
