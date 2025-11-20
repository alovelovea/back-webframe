# apis/scripts/load_all_data.py

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANAGE_PY = os.path.join(os.path.dirname(BASE_DIR), '..', 'manage.py')

def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    print(f"\n🔥 Running {script_name} ...")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode == 0:
        print(f"✅ Success: {script_name}")
    else:
        print(f"❌ Failed: {script_name}")

def main():
    print("========================================")
    print("🚀 Starting full database data load...")
    print("========================================\n")

    load_order = [
        "load_allergy_data.py",
        "load_ingredient_data.py",
        "load_person_data.py",
        "load_personAllergy_data.py",
        "load_allergyIngredient_data.py",
        "load_recipe_data.py",
        "load_recipeIngredient_data.py",
        "load_fridge_data.py",
        "load_like_data.py",
        "load_shopping_data.py",
    ]

    for script in load_order:
        run_script(script)

    print("\n========================================")
    print("🎉 ALL DATA LOADED SUCCESSFULLY!")
    print("========================================")

if __name__ == "__main__":
    main()
