import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

import threading
from interaction import Massar


class MassarApp:
    def __init__(self, root):
        self.root = root
        global_font = tkFont.Font(family="Arial", size=16)
        self.root.option_add("*Font", global_font)
        self.massar = ""
        self.root.title("Massar Absence Checker")

        self.label_month = tk.Label(root, text="📅 Mois:")
        self.label_month.pack(pady=5)
        self.entry_month = tk.Entry(root)
        self.entry_month.pack(pady=5)

        self.label_class = tk.Label(root, text="🏫 Nom de classe:")
        self.label_class.pack(pady=5)
        self.entry_class = tk.Entry(root)
        self.entry_class.pack(pady=5)

        self.label_eleve = tk.Label(root, text=" Eleve:")
        self.label_eleve.pack(pady=5)
        self.entry_eleve = tk.Entry(root)
        self.entry_eleve.pack(pady=5)


        self.btn_start = tk.Button(root, text="🚀 Lancer", command=self.start_process)
        self.btn_start.pack(pady=10)

        self.log = tk.Text(root, height=10, width=50)
        self.log.pack(pady=10)

    def log_message(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def start_process(self):
        mois = self.entry_month.get().strip()
        nom_classe = self.entry_class.get().strip()
        eleve = self.entry_eleve.get().strip()

        if not mois or not nom_classe:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        threading.Thread(target=self.run_massar, args=(mois, nom_classe, eleve), daemon=True).start()

    def run_massar(self, mois, nom_classe, eleve):
        self.log_message("🔄 Démarrage du processus...")
        # print(mois, nom_classe, eleve)
        if self.massar == "":
            self.massar = Massar()
            if self.massar.main_interaction():
                self.log_message("✅ Connexion réussie.")
                self.massar.get_absence_site()
                self.log_message("🔍 Recherche d'absences...")
                self.massar.main_loop(nom_class=nom_classe, month=mois, eleve=eleve, log_message = self.log_message)
                self.log_message("📋 Terminé.")
            else:
                self.log_message("❌ Échec de la connexion.")
        else:
            try:
                self.log_message("🔍 Recherche d'absences...")
                self.massar.main_loop(nom_class=nom_classe, month=mois, eleve=eleve, log_message=self.log_message)
                self.log_message("📋 Terminé.")
            except Exception as e:
                print(e)
                self.massar.exit_program()
                print("Trying again...")
                self.massar = Massar()
                if self.massar.main_interaction():
                    self.log_message("✅ Connexion réussie.")
                    self.massar.get_absence_site()
                    self.log_message("🔍 Recherche d'absences...")
                    self.massar.main_loop(nom_class=nom_classe, month=mois, eleve=eleve, log_message=self.log_message)
                    self.log_message("📋 Terminé.")
                else:
                    self.log_message("❌ Échec de la connexion.")





        # m.exit_program()

if __name__ == "__main__":
    root = tk.Tk()
    app = MassarApp(root)
    root.mainloop()