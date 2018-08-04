from rest_framework.routers import DefaultRouter

# from django.conf.urls import include, url

from .views import UserViewSet

app_name = 'accounts'

# # Here the comments and activity is added manually by including
# them under the detail view.
#
# urlpatterns = [
#
#     url(
#         regex=r'^$',
#         view=UserViewSet.as_view({'get': 'list'}),
#         name='user-list'
#     ),
#
#     url(
#         r'^(?P<pk>[\w.@+-]+)/',
#         include([
#             url(
#                 regex=r'^$',
#                 view=UserViewSet.as_view({'get': 'retrieve'}),
#                 name='user-detail'
#             ),
#             url(
#                 regex=r'^comments/$',
#                 view=UserViewSet.as_view({'get': 'comments',
#                  'post': 'comments'}),
#                 name='user-comments'
#             ),
#             url(
#                 regex=r'^activities/$',
#                 view=UserViewSet.as_view({'get': 'activities'}),
#                 name='user-activities'
#             ),
#         ])
#     ),
#
# ]


# urlpatterns = [
#     url(_(r'^register/$'),
#         accounts.views.UserRegisterView.as_view(),
#         name='register'),
#     url(_(r'^login/$'),
#         accounts.views.UserLoginView.as_view(),
#         name='login'),
#     url(_(r'^confirm/email/(?P<activation_key>.*)/$'),
#         accounts.views.UserConfirmEmailView.as_view(),
#         name='confirm_email'),
#     url(_(r'^status/email/$'),
#         accounts.views.UserEmailConfirmationStatusView.as_view(),
#         name='status'),

# ]

# If we use a router the comments and activity is added via
# the @detail_route decorator in the CommentsMixin and ActivitiesMixin.
# This means, that nothing has to be changed here.

router = DefaultRouter()
router.register(r'', UserViewSet)
urlpatterns = router.urls
