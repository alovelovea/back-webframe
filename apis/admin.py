from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Person, Allergy, PersonAllergy, Ingredient, AllergyIngredient,
    Fridge, Recipe, RecipeIngredient, Like
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
from urllib.parse import quote

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient_id', 'ingredient_name', 'unit', 'ingredient_category', 'price', 'preview_image')
    list_filter = ('ingredient_category',)
    search_fields = ('ingredient_name',)

    def preview_image(self, obj):
        if obj.ingredient_img:
            img_path = obj.ingredient_img
            if not img_path.startswith("media/") and not img_path.startswith("/media/"):
                img_path = f"/media/{img_path}"

            # ✅ 괄호, 공백 등 특수문자 인코딩
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
    list_display = ('fridge_id', 'person', 'ingredient', 'f_quantity', 'exdate')
    list_filter = ('exdate',)
    search_fields = ('person__name', 'ingredient__ingredient_name')


# ------------------------------
# 7. Recipe (레시피)
# ------------------------------
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe_id', 'recipe_name', 'recipe_category', 'preview_image')
    search_fields = ('recipe_name', 'recipe_category')

    # ✅ 레시피 이미지 미리보기
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
