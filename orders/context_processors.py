def breadcrumbs(request):
    # Generates a list of breadcrumbs items based on the request path.
    # Each breadcrumb is a dictionary with 'name' and 'url'.
    path_parts = request.path.strip("/").split("/")
    breadcrumbs_list = []
    accumulated_path = ""

    for part in path_parts:
        if part:
            accumulated_path += f"/{part}"
            breadcrumbs_list.append({
                "name": part.replace("-", " ")..capitalize(),
                "url": accumulated_path
            })

    return {"breadcrumbs": breadcrumbs_list}