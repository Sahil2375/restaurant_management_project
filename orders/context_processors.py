def breadcrumbs(request):
    # Generates a list of breadcrumbs items based on the request path.
    # Each breadcrumb is a dictionary with 'name' and 'url'.
    path = request.path.strip("/").split("/")
    breadcrumbs_list = []
    accumulated_path = ""

    for segment in path:
        if segment: # avoid empty strings
            accumulated_path += f"/{segment}"
            breadcrumbs_list.append({
                "name": segment.replace("-", " ")..capitalize(),
                "url": accumulated_path
            })

    return {"breadcrumbs": breadcrumbs_list}