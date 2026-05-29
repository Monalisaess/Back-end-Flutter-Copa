# Publicar no GitHub — Back-end

Repositório: https://github.com/Monalisaess/Back-end-Flutter-Copa

## Primeira vez (na pasta do back-end)

```powershell
cd C:\Users\Monal\Downloads\Back-end-Flutter-Copa

git init
git branch -M main
git remote add origin https://github.com/Monalisaess/Back-end-Flutter-Copa.git

git add .
git status
```

Confirme que **`.env` não aparece** no status (só `.env.example`).

```powershell
git commit -m "Adiciona API Flask modular alinhada ao app Flutter"
git push -u origin main
```

Se o remoto já tiver README/LICENSE e der conflito:

```powershell
git pull origin main --allow-unrelated-histories
# Resolva conflitos se houver, depois:
git push -u origin main
```

## Atualizar depois

```powershell
git add .
git commit -m "Sua mensagem"
git push
```
