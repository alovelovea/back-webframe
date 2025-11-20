from django.contrib import admin
from django.utils.html import format_html
from urllib.parse import quote
from .models import (
    Person, Allergy, PersonAllergy, Ingredient, AllergyIngredient,
    Fridge, Recipe, RecipeIngredient, Like, Shopping
)

# ------------------------------
# 1. Person (사용자)
# ------------------------------
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('p_id', 'user_id', 'name', 'is_vegan')
    search_fields = ('user_id', 'name')
    list_filter = ('is_vegan',)

# ------------------------------
# 2. Allergy (알러지)
# ------------------------------
@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('allergy_id', 'allergy_name')
    search_fields = ('allergy_name',)

# ------------------------------
# 3. PersonAllergy
# ------------------------------
@admin.register(PersonAllergy)
class PersonAllergyAdmin(admin.ModelAdmin):
    list_display = ('person', 'allergy')
    list_filter = ('allergy',)
    search_fields = ('person__name', 'allergy__allergy_name')

# ------------------------------
# 4. Ingredient (식재료)
# ------------------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient_id', 'ingredient_name', 'unit', 
        'ingredient_category', 'price', 'shelf_life', 'preview_image'
    )
    list_filter = ('ingredient_category',)
    search_fields = ('ingredient_name',)

    def preview_image(self, obj):
        if obj.ingredient_img:
            img_path = obj.ingredient_img
            if not img_path.startswith("media/") and not img_path.startswith("/media/"):
                img_path = f"/media/{img_path}"

            encoded_path = quote(img_path)
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:8px;" />',
                encoded_path
            )
        return "❌ 없음"

    preview_image.short_description = "이미지 미리보기"

# ------------------------------
# 5. AllergyIngredient
# ------------------------------
@admin.register(AllergyIngredient)
class AllergyIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'allergy')
    search_fields = ('ingredient__ingredient_name', 'allergy__allergy_name')

# ------------------------------
# 6. Fridge (냉장고)
# ------------------------------
@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    list_display = (
        'fridge_id', 'person', 'ingredient', 
        'f_quantity', 'added_date', 'expiry_date'
    )
    list_filter = ('expiry_date',)
    search_fields = ('person__name', 'ingredient__ingredient_name')

# ------------------------------
# 7. Recipe (레시피)
# ------------------------------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'recipe_name', 'recipe_category', 'preview_image')
    search_fields = ('recipe_name', 'recipe_category')

    def preview_image(self, obj):
        if obj.recipe_img:
            return format_html(
                '<img src="/media/{}" style="width:80px; height:80px; object-fit:cover; border-radius:8px;" />',
                obj.recipe_img
            )
        return "❌ 없음"

    preview_image.short_description = "이미지 미리보기"

# ------------------------------
# 8. RecipeIngredient
# ------------------------------
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'r_quantity')
    search_fields = ('recipe__recipe_name', 'ingredient__ingredient_name')

# ------------------------------
# 9. Like (좋아요)
# ------------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'person')
    search_fields = ('recipe__recipe_name', 'person__name')

# ------------------------------
# 10. Shopping (쇼핑 기록)
# ------------------------------  

@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'shopping_id',
        'person',
        'ingredient',
        'quantity',
        'unit_price',      # ✔ 자동 계산
        'price',           # ✔ 자동 계산
        'purchased_date',
        'added_to_fridge',
        'fridge_record'
    )

    list_filter = (
        'purchased_date',
        'added_to_fridge',
        'ingredient__ingredient_category'
    )

    search_fields = (
        'person__name',
        'person__user_id',
        'ingredient__ingredient_name'
    )

    ordering = ('-purchased_date',)

    # ✔ 자동 계산 필드 수정 금지
    readonly_fields = (
        'unit_price',
        'price',
        'added_to_fridge',
        'fridge_record'
    )