from django.urls import path
from .views import (
    login_user,
    signup_user,
    classify_query_view,
    my_fridge,
    add_ingredient,
    delete_ingredient,
    toggle_like,
    fridge_items_api,
    recipe_list_api,   
    add_recipe,
    ingredient_list
)

urlpatterns = [
    path('login/', login_user, name='login_user'),
    path('signup/', signup_user, name='signup_user'),
    path('fridge_items/', fridge_items_api, name='fridge_items_api'),
    path('classify/', classify_query_view, name='classify_query'),

    # 🔥 레시피 리스트 + 레시피 추가 API 등록
    path('recipes/', recipe_list_api, name='recipe_list_api'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('ingredients/', ingredient_list, name='ingredient_list'),

    # 냉장고 기능
    path('my_fridge/', my_fridge, name='my_fridge'),
    path('add_ingredient/', add_ingredient, name='add_ingredient'),
    path('delete_ingredient/<int:fridge_id>/', delete_ingredient, name='delete_ingredient'),
    path('toggle_like/<int:recipe_id>/', toggle_like, name='toggle_like'),
]
