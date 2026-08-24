[app]

# Título do aplicativo
title = Ditado Game

# Nome do pacote
package.name = ditadogame

# Domínio do pacote
package.domain = org.ditadogame

# Pasta principal do projeto
source.dir = .

# Arquivos incluídos no APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3,txt

# Versão do aplicativo
version = 1.0

# Dependências
requirements = python3,kivy==2.3.1

# Orientação
orientation = portrait

# Tela cheia
fullscreen = 0

# Versão mínima do Android
android.minapi = 24

# Arquiteturas
android.archs = arm64-v8a,armeabi-v7a

# Backend gráfico
android.add_src =

# Nome do arquivo APK
android.entrypoint = org.kivy.android.PythonActivity


[buildozer]

# Nível de log
log_level = 2

# Não executar como root
warn_on_root = 1
