import os


def models_capitalize(models):
    models_capitalize = [model.capitalize() for model in models]
    return models_capitalize


def create_app(project_name, app_name):
    if not os.path.isdir(f"./{project_name}/{app_name}"):
        os.mkdir(f"./{project_name}/{app_name}")
        os.chdir(f"./{project_name}/{app_name}")
        files = ("__init__.py", "models.py",
                 "serializers.py", "views.py")
        for file in files:
            open(file, "w+")

        list_models = []
        while True:
            model_name = input("Digite o nome do model: ")
            list_models.append(model_name)
            option = int(input('''1 para continuar\n2 para sair '''))
            if option == 2:
                break

        models_cap = models_capitalize(list_models)
        models_joined = ', '.join(models_cap)
        models_joined_serializer = 'Serializer, '.join(models_cap)
        models_joined_views = 'View, '.join(models_cap)

        models = open("models.py", "a+")
        models.writelines(
            ["from django.db import models\n",
             "\n",
             "\n"]
        )
        views = open("views.py", "a+")
        views.writelines(
            ["from rest_framework import viewsets\n",
                f"from {project_name}.{app_name}.models import {models_joined}\n",
                f"from {project_name}.{app_name}.serializers import {models_joined_serializer}Serializer\n",
                "\n",
                "\n"])

        serializers = open("serializers.py", "a+")
        serializers.writelines(
            [f"from rest_framework import serializers\n",
                f"from {project_name}.{app_name}.models import {models_joined}\n",
                "\n",
                "\n"
             ])

        for model in models_cap:
            with open("models.py", "a+") as models:
                models.writelines(
                    [f"class {model}(models.Model):\n",
                     "    pass\n",
                     "\n"]
                )

            with open("views.py", "a+") as views:
                views.writelines(
                    [f"class {model}ViewSet(viewsets.ModelViewSet):\n",
                     f"    queryset = {model}.objects.all()\n",
                     f"    serializer_class = {model}Serializer\n",
                     "\n"])

            with open("serializers.py", "a+") as serializers:
                serializers.writelines(
                    [f"class {model}Serializer(serializers.ModelSerializer):\n",
                     "    class Meta:\n",
                     f"        model = {model}\n",
                     "        fields = '__all__'\n",
                     "\n"])

    else:
        print("App já existe")

    os.chdir(f'..')

    urls = open('urls.py', 'r')
    lines = urls.readlines()
    lines.insert(
        21, f"from {project_name}.{app_name}.views import {models_joined_views}View\n\n")
    urls.close()
    urls = open('urls.py', 'w')
    urls.writelines(lines)
    urls.close()

    for model in models_cap:
        urls = open('urls.py', 'r')
        lines = urls.readlines()
        lines.insert(
            26, f'router.register(r"api/v1/{model.lower()}", {model}View)\n')
        urls.close()
        urls = open('urls.py', 'w')
        urls.writelines(lines)
        urls.write('\n')
        urls.close()


if __name__ == "__main__":
    project_name = input("Qual o nome do projeto? ")
    app_name = input("Digite o nome do app: ")
    create_app(project_name, app_name)
