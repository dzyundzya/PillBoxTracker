from django.urls import path

from pillbox import views


app_name = 'pillbox'

urlpatterns = [
    path(
        'category/<slug:category_slug>/', views.CategoryListView.as_view(), 
        name='category_pills'
    ),
    path('pills/create/', views.PillCreateView.as_view(), name='create_pill'),
    path('pills/<int:pill_id>/', views.PillDetailView.as_view(), name='pill_detail'),
    path('pills/<int:pill_id>/edit/', views.PillUpdateView.as_view(), name='edit_pill'),
    path('pills/<int:pill_id>/delete/', views.PillDeleteView.as_view(), name='delete_pill'),
    path('pills/<int:pill_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('pills/<int:pill_id>/edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('pills/<int:pill_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('admin-profile/<str:username>/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('pillbox/create/', views.PillBoxCreateView.as_view(), name='create_pillbox'),
]
