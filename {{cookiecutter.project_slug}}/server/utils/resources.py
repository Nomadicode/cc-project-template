def retrieve_resource(resource=None, retrieve_fields={'pk': None}):
    try:
        instance = resource.objects.get(**retrieve_fields)
    except resource.DoesNotExist:
        return None, False
    
    return instance, True
