# RetenIA

## Como usar Git y GitHub
1. Clonar repositorio
```
git clone https://github.com/L4rralde/RetenIA.git
source RetenIA/setup.bash
```
2. Acceder al repositorio rapidamente:
```
cd $REPO_PATH
```

**En las siguientes instrucciones tienes que estar dentro del repositorio**

3. Actualizar repositorio 
```
git pull
```
4. Revisar cambiosen el repositorio
```
git status
```
o
```
git status <ruta_de_archivo_o_directorio>
```
Si quieres ver los cambios que has hecho de un archivo o directorio exclusivamente

5. Incluir cambios
```
git add <ruta_de_archivo_o_directorio>
```

6. Hacer checkpoint local de tus cambios incluidos
```
git pull 
git commit -m "<Descripcion_del_commit>"
```

7. Subir todos tus checkpoints a remoto
```
git push
```
Este paso te pedira usuario y contrasena. La contrasenia es un token *classic*. Lo puedes generar [asi](https://www.youtube.com/watch?v=Nl4qwzXydQ0)

8. Guardar token
Este paso se hace una sola vez.
```
git config credential.helper store
```

## DataSet
**Nunca añadas nada del directorio ./DataSet. Es sólo un placeholder**

En este [enlace](https://drive.google.com/drive/folders/1rQFvU_iIsVMYDO_vthsNkF4hyJyiXz8w?usp=share_link) se agregarán videos, rosbags y modelos.

## TODO (cosas por hacer):
- [ ] Usar una cuenta de drive para subir datos generados (videos, rosbags, modelos de algoritmos como Redes neuronales de detección)
- [ ] Agregar todos nuestros contactos.

## Contactos:
- Braulio:
	
- Emmanuel Larralde:
	> ealarralde@gmail.com
	> @L4rralde
- Lamberto Vázquez:
	> Lamberto00@hotmail.com
	> @Lambert00
- Raúl Romero:
	> rullyromerol@gmail.com
	> @3xR-L