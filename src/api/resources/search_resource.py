from .base_resource import BaseResource


class StartWithQuery(BaseResource):

    def get(self, query):
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
