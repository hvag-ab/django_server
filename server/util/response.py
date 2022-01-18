from rest_framework.response import Response


class JsResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, code=True, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        data = {"success": code, "data": data, "message": msg}
        super().__init__(data=data, status=status,
                 template_name=template_name, headers=headers,
                 exception=exception, content_type=content_type)



