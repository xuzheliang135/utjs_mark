from flask import render_template
from . import web


@web.app_errorhandler(403)
def page_not_found(e):
    """
        AOP，处理所有的403请求
    """
    return render_template('403.html'), 403

# @web.app_errorhandler(404)
# def page_not_found(e):
#     """
#         AOP，处理所有的404请求
#     """
#     return render_template('404.html'), 404


# @web.app_errorhandler(500)
# def internal_server_error(e):
#     """
#         AOP，处理所有的500请求
#     """
#     if request.accept_mimetypes.accept_json and \
#             not request.accept_mimetypes.accept_html:
#         # unkown = UnknownException().get_args()
#         # response = jsonify(unkown['message'])
#         response = jsonify('asd')
#         response.status_code = 500
#         return response
#     return render_template('500.html'), 500
