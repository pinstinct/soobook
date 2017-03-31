# __all__ = (
#     'LogoutView',
# )


# class LogoutView(RestLogoutView):
#     def logout(self, request):
#         try:
#             request.user.auth_token.delete()
#         except (AttributeError, ObjectDoesNotExist):
#             return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
#
#         django_logout(request)
#         return Response({"detail": _("Successfully logged out.")},
#                         status=status.HTTP_200_OK)
