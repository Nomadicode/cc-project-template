def retrieve_resource(resource=None, retrieve_field='pk', value=None):
    fields = {}
    fields[retrieve_field] = value
    try:
        instance = resource.objects.get(**fields)
    except resource.DoesNotExist:
        return None, False
    
    return instance, True


def retrieve_resource_multiple_param(resource=None, retrieve_fields={"pk": None}):
    try:
        instance = resource.objects.get(**retrieve_fields)
    except resource.DoesNotExist:
        return None, False
    
    return instance, True
