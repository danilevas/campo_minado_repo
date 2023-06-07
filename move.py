import shutil
import os
import zipfile
import glob

path = "C:/Programas/Projetos Pessoais/tkinter/"

def copia_pra_fora():
    if os.path.exists(path + "campo_minado_files"):
        deleta_cont_pasta(path + "campo_minado_files")
    else:
        os.mkdir(path + "campo_minado_files")
    
    if os.path.exists(path + "icones"):
        deleta_cont_pasta(path + "icones")
        os.rmdir(path + "icones")
    copia_pasta(path + "campo_minado_repo/icones", "icones", path)

    if os.path.exists(path + "sons"):
        deleta_cont_pasta(path + "sons")
        os.rmdir(path + "sons")
    copia_pasta(path + "campo_minado_repo/sons", "sons", path)

    if os.path.exists(path + "campo_minado.pyw"):
        os.remove(path + "campo_minado.pyw")
    shutil.copy(path + "campo_minado_repo/campo_minado.pyw", path)

    if os.path.exists(path + "center.py"):
        os.remove(path + "center.py")
    shutil.copy(path + "campo_minado_repo/center.py", path)
    
    # shutil.copy(path + "campo_minado_repo/campo_minado.exe", path)
    
def movimenta():
    copia_pasta(path + "icones", "icones", path + "campo_minado_files")
    deleta_cont_pasta(path + "icones")
    os.rmdir(path + "icones")
    copia_pasta(path + "sons", "sons", path + "campo_minado_files")
    deleta_cont_pasta(path + "sons")
    os.rmdir(path + "sons")
    shutil.copy(path + "campo_minado.pyw", path + "campo_minado_files")
    os.remove(path + "campo_minado.pyw")
    shutil.copy(path + "center.py", path + "campo_minado_files")
    os.remove(path + "center.py")
    shutil.copy(path + "campo_minado.exe", path + "campo_minado_files")
    os.remove(path + "campo_minado.exe")

def copia_pasta(path_pasta, nome_pasta, destino):
    nova_pasta = destino + "/" + nome_pasta
    os.mkdir(nova_pasta)
    path_pasta = path_pasta + "/"
    for file_name in os.listdir(path_pasta):
        source = path_pasta + file_name
        destination = nova_pasta

        if os.path.isfile(source):
            shutil.copy(source, destination)
            print('copied', file_name)
        else:
            copia_pasta(source, file_name, destination)
            print('copied', file_name)

def deleta_cont_pasta(pasta):
    pasta = pasta + "/"
    for file_name in os.listdir(pasta):
        file_path = pasta + file_name

        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                deleta_cont_pasta(file_path)
                os.rmdir(file_path)
            print('removido', file_name)

def maneja_exe():
    if os.path.exists(path + "build"):
        deleta_cont_pasta(path + "build")
        os.rmdir(path + "build")
    if os.path.exists(path + "campo_minado.spec"):
        os.remove(path + "campo_minado.spec")
    if os.path.exists(path + "dist"):
        shutil.copy(path + "dist/campo_minado.exe", path)
        deleta_cont_pasta(path + "dist")
        os.rmdir(path + "dist")

def zipa_files():
    with zipfile.ZipFile('campo_minado_files.zip', 'w') as f:
        for file in glob.glob('campo_minado_files/*'):
            f.write(file)

def unzipa_files(arquivo_zip):
    with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
        zip_ref.extractall()

copia_pra_fora()
if os.path.exists(path + "campo_minado.exe"):
    os.remove(path + "campo_minado.exe")
os.system('pyinstaller.exe --onefile --icon=icones/bomba.ico campo_minado.pyw')
maneja_exe()
movimenta()
if os.path.exists(path + "campo_minado_files.zip"):
    os.remove(path + "campo_minado_files.zip")
zipa_files()
shutil.copy(path + "campo_minado_files.zip", path + "campo_minado_repo")
if os.path.exists(path + "campo_minado_repo/campo_minado_files"):
    deleta_cont_pasta(path + "campo_minado_repo/campo_minado_files")
    os.rmdir(path + "campo_minado_repo/campo_minado_files")
copia_pasta(path + "campo_minado_files", "campo_minado_files", path + "campo_minado_repo")