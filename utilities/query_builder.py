def buildElsQuery(must=None, should=None, must_not=None, mustExpression=None, mustNotExpression=None,
                  shouldExpression=None):
    query = {"query": {"bool": {}}}
    if must:
        query["query"]["bool"]["must"] = [{"match": {key: value}} for key, value in must.items()]
    if mustExpression:
        if not isinstance(mustExpression, list):
            mustExpression = [mustExpression]
        for exp in mustExpression:
            if "must" not in query["query"]["bool"]:
                query["query"]["bool"]["must"] = []
            query["query"]["bool"]["must"].extend([{key: value} for key, value in exp.items()])
    if should:
        shouldQuery = []
        for key, value in should.items():
            shouldQuery.extend([{"match": {key: v}} for v in value])
        if shouldExpression:
            shouldQuery.extend([{key: value} for key, value in shouldExpression.items()])
        if shouldQuery:
            if must:
                query["query"]["bool"]["must"].append({"bool": {"should": shouldQuery}})
            else:
                query["query"]["bool"]["should"] = shouldQuery
    elif shouldExpression:
        shouldQuery = []
        # shouldQuery = [{key: value} for key, value in shouldExpression.items()]
        if shouldExpression:
            if not isinstance(shouldExpression, list):
                shouldExpression = [shouldExpression]
            for exp in shouldExpression:
                shouldQuery.extend([{key: value} for key, value in exp.items()])
        if shouldQuery:
            if must:
                query["query"]["bool"]["must"].append({"bool": {"should": shouldQuery}})
            else:
                query["query"]["bool"]["should"] = shouldQuery
    if must_not:
        query["query"]["bool"]["must_not"] = [{"match": {key: value}} for key, value in must_not.items()]
    if mustNotExpression:
        if not query["query"]["bool"].get("must_not"):
            query["query"]["bool"]["must_not"] = []
        if not isinstance(mustNotExpression, list):
            mustNotExpression = [mustNotExpression]
        for exp in mustNotExpression:
            query["query"]["bool"]["must_not"].extend([{key: value} for key, value in exp.items()])
    return query