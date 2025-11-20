from django.db import models

# ------------------------------
# 1. 사용자 (Person)
# ------------------------------
class Person(models.Model):
    p_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password_2 = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    is_vegan = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ------------------------------
# 2. 알러지 (Allergy)
# ------------------------------
class Allergy(models.Model):
    allergy_id = models.AutoField(primary_key=True)
    allergy_name = models.CharField(max_length=50)

    def __str__(self):
        return self.allergy_name


# ------------------------------
# 3. 사용자-알러지 관계 (PersonAllergy)
# ------------------------------
class PersonAllergy(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, to_field='p_id')
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'allergy')



# ------------------------------
# 4. 식재료 (Ingredient)
# ------------------------------
class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100)
    ingredient_img = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=20)
    ingredient_category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # 🆕 추가: 유지기간 (일)
    shelf_life = models.IntegerField(default=3)  # ex) 3일, 5일, 7일 등

    def __str__(self):
        return self.ingredient_name



# ------------------------------
# 5. 알러지-식재료 관계 (AllergyIngredient)
# ------------------------------
class AllergyIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ingredient', 'allergy')



# ------------------------------
# 6. 냉장고 (Fridge)
# ------------------------------
from datetime import timedelta

class Fridge(models.Model):
    fridge_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, to_field='p_id')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    f_quantity = models.DecimalField(max_digits=8, decimal_places=2)

    # 🆕 추가: 냉장고에 넣은 날짜
    added_date = models.DateField(null=True, blank=True)

    # 🆕 수정: 유통기한 (자동 계산된 값)
    expiry_date = models.DateField(null=True, blank=True)


    def save(self, *args, **kwargs):
        """added_date + ingredient.shelf_life로 expiry_date 자동 계산"""
        if self.added_date and self.ingredient.shelf_life:
            self.expiry_date = self.added_date + timedelta(days=self.ingredient.shelf_life)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person.name} - {self.ingredient.ingredient_name}"



# ------------------------------
# 7. 레시피 (Recipe)
# ------------------------------
class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    recipe_img = models.CharField(max_length=200, blank=True, null=True)
    recipe_category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.recipe_name


# ------------------------------
# 8. 레시피-재료 관계 (RecipeIngredient)
# ------------------------------
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    r_quantity = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ('recipe', 'ingredient')


# ------------------------------
# 9. 좋아요 (Like)
# ------------------------------
class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, to_field='p_id')

    class Meta:
        unique_together = ('recipe', 'person')

class Shopping(models.Model):
    shopping_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    purchased_date = models.DateField()

    added_to_fridge = models.BooleanField(default=False)
    fridge_record = models.ForeignKey(
        'Fridge',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        # 🔥 INSERT 되기 전에 1회만 계산
        if not self.pk:
            self.unit_price = self.ingredient.price
            self.price = self.unit_price * self.quantity

        super().save(*args, **kwargs)

        # 🔥 두 번째 INSERT 방지 / fridge 자동생성은 UPDATE에서만 수행
        if not self.added_to_fridge:
            fridge_item = Fridge.objects.create(
                person=self.person,
                ingredient=self.ingredient,
                f_quantity=self.quantity,
                added_date=self.purchased_date,
            )

            self.fridge_record = fridge_item
            self.added_to_fridge = True

            # 🔥 UPDATE만 수행
            super().save(update_fields=['fridge_record', 'added_to_fridge'])

    def __str__(self):
        return f"{self.person.name}의 구매: {self.ingredient.ingredient_name}"

