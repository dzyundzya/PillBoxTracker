from django.urls import path

from pillbox import views


app_name = 'pillbox'

urlpatterns = [
    path('pills/create/', views.PillCreateView.as_view(), name='create_pill'),
    path('pills/<int:pill_id>/', views.PillDetailView.as_view(), name='pill_detail'),
    path('pills/<int:pill_id>/edit/', views.PillUpdateView.as_view(), name='edit_pill'),
    path('pills/<int:pill_id>/delete/', views.PillDeleteView.as_view(), name='delete_pill'),
    path('pills/<int:pill_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('pills/<int:pill_id>/edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('pills/<int:pill_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
]