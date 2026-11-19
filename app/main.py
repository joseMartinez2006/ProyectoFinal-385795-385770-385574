import tkinter as tk
from tkinter import messagebox, simpledialog

from auth import login_user, register_user

from blog import (
    get_articles,
    create_article,
    update_article,
    delete_article,
    get_comments,
    create_comment,
    update_comment,
    delete_comment,
    create_tag,
    get_tags,
    update_tag,
    delete_tag,
    create_category,
    get_categories,
    update_category,
    delete_category
)


class BlogApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Blog Manager")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.user = None
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # INICIO DE SESION

    def show_login(self):
        self.clear_window()
        self.root.geometry("600x450")

        tk.Label(
            self.root,
            text="BLOG MANAGER",
            font=("Arial", 22, "bold")
        ).pack(pady=30)

        tk.Label(self.root, text="Correo electronico").pack()
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Contrasena").pack()
        self.password_entry = tk.Entry(
            self.root, width=35, show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Iniciar sesion",
            width=25,
            command=self.login
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Crear cuenta",
            width=25,
            command=self.show_register
        ).pack()

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingresa tu correo y contrasena."
            )
            return

        user = login_user(email, password)

        if user:
            self.user = user
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Error",
                "Correo o contrasena incorrectos."
            )

    # REGISTRO

    def show_register(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="CREAR CUENTA",
            font=("Arial", 20, "bold")
        ).pack(pady=25)

        tk.Label(self.root, text="Nombre").pack()
        self.name_entry = tk.Entry(self.root, width=35)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Correo electronico").pack()
        self.email_entry = tk.Entry(self.root, width=35)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Contrasena").pack()
        self.password_entry = tk.Entry(
            self.root, width=35, show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Registrarse",
            width=25,
            command=self.register
        ).pack(pady=15)

        tk.Button(
            self.root,
            text="Volver al inicio",
            width=25,
            command=self.show_login
        ).pack()

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos."
            )
            return

        if register_user(name, email, password):
            messagebox.showinfo(
                "Registro exitoso",
                "Tu cuenta ha sido creada."
            )
            self.show_login()
        else:
            messagebox.showerror(
                "Error",
                "No fue posible crear la cuenta."
            )

    # PANEL PRINCIPAL

    def show_dashboard(self):
        self.clear_window()
        self.root.geometry("800x700")

        tk.Label(
            self.root,
            text="BLOG MANAGER",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        tk.Label(
            self.root,
            text=f"Bienvenido, {self.user['name']} | "
                 f"Rol: {self.user['role'].upper()}"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text="ARTICULOS",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.article_list = tk.Listbox(
            self.root,
            width=85,
            height=13
        )
        self.article_list.pack(pady=10)

        tk.Button(
            self.root,
            text="Crear articulo",
            width=30,
            command=self.create_article_window
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Modificar articulo",
            width=30,
            command=self.edit_article_window
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Eliminar articulo",
            width=30,
            command=self.delete_selected_article
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Administrar comentarios",
            width=30,
            command=self.show_comments
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Administrar etiquetas y categorias",
            width=30,
            command=self.manage_tags_categories
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Actualizar lista",
            width=30,
            command=self.load_articles
        ).pack(pady=3)

        tk.Button(
            self.root,
            text="Cerrar sesion",
            width=30,
            command=self.logout
        ).pack(pady=10)

        self.load_articles()

    def load_articles(self):
        self.article_list.delete(0, tk.END)
        self.articles = get_articles()

        for article in self.articles:
            self.article_list.insert(
                tk.END,
                f"{article['title']} - {article['date']}"
            )

    # CREAR ARTICULOS

    def create_article_window(self):
        window = tk.Toplevel(self.root)
        window.title("Crear articulo")
        window.geometry("450x400")

        tk.Label(window, text="Titulo").pack(pady=5)
        title_entry = tk.Entry(window, width=45)
        title_entry.pack(pady=5)

        tk.Label(window, text="Contenido").pack(pady=5)
        content_text = tk.Text(window, width=45, height=12)
        content_text.pack(pady=5)

        def save_article():
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()

            if not title or not content:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Ingresa el titulo y el contenido."
                )
                return

            article_id = create_article(
                self.user["email"],
                title,
                content
            )

            if article_id:
                messagebox.showinfo(
                    "Exito",
                    "Articulo creado correctamente."
                )
                window.destroy()
                self.load_articles()
            else:
                messagebox.showerror(
                    "Error",
                    "No fue posible crear el articulo."
                )

        tk.Button(
            window,
            text="Guardar articulo",
            command=save_article
        ).pack(pady=10)

    # MODIFICAR ARTICULOS

    def edit_article_window(self):
        selection = self.article_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un articulo."
            )
            return

        article = self.articles[selection[0]]

        window = tk.Toplevel(self.root)
        window.title("Modificar articulo")
        window.geometry("450x400")

        tk.Label(window, text="Titulo").pack(pady=5)
        title_entry = tk.Entry(window, width=45)
        title_entry.pack(pady=5)
        title_entry.insert(0, article["title"])

        tk.Label(window, text="Contenido").pack(pady=5)
        content_text = tk.Text(window, width=45, height=12)
        content_text.pack(pady=5)
        content_text.insert("1.0", article["text"])

        def save_changes():
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()

            if not title or not content:
                messagebox.showwarning(
                    "Datos incompletos",
                    "Completa todos los campos."
                )
                return

            success = update_article(
                article["id"],
                title,
                content,
                self.user["email"],
                self.user["role"]
            )

            if success:
                messagebox.showinfo(
                    "Exito",
                    "Articulo actualizado."
                )
                window.destroy()
                self.load_articles()
            else:
                messagebox.showerror(
                    "Error",
                    "No tienes permiso para modificar este articulo."
                )

        tk.Button(
            window,
            text="Guardar cambios",
            command=save_changes
        ).pack(pady=10)

    # ELIMINAR ARTICULOS

    def delete_selected_article(self):
        selection = self.article_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un articulo."
            )
            return

        article = self.articles[selection[0]]

        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Deseas eliminar el articulo '{article['title']}'?"
        )

        if not confirm:
            return

        success = delete_article(
            article["id"],
            self.user["email"],
            self.user["role"]
        )

        if success:
            messagebox.showinfo("Exito", "Articulo eliminado.")
            self.load_articles()
        else:
            messagebox.showerror(
                "Error",
                "No tienes permiso para eliminar este articulo."
            )

    # COMENTARIOS

    
    def show_comments(self):
        selection = self.article_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un articulo."
            )
            return

        article = self.articles[selection[0]]

        window = tk.Toplevel(self.root)
        window.title("Comentarios")
        window.geometry("600x500")

        tk.Label(
            window,
            text=f"Comentarios de: {article['title']}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        comment_list = tk.Listbox(
            window,
            width=75,
            height=12
        )
        comment_list.pack(pady=10)

        comments = []

        def refresh_comments():
            nonlocal comments

            comment_list.delete(0, tk.END)
            comments = get_comments(article["id"])

            for comment in comments:
                comment_list.insert(
                    tk.END,
                    f"{comment['author']}: {comment['content']}"
                )

        def add_comment():
            comment_window = tk.Toplevel(window)
            comment_window.title("Agregar comentario")
            comment_window.geometry("400x300")

            tk.Label(
                comment_window,
                text="Escribe tu comentario:"
            ).pack(pady=10)

            content_text = tk.Text(
                comment_window,
                width=42,
                height=9
            )
            content_text.pack(padx=10, pady=5)

            def save_comment():
                content = content_text.get(
                    "1.0", tk.END
                ).strip()

                if not content:
                    messagebox.showwarning(
                        "Datos incompletos",
                        "Escribe el contenido del comentario."
                    )
                    return

                comment_id = create_comment(
                    self.user["email"],
                    article["id"],
                    content
                )

                if comment_id:
                    messagebox.showinfo(
                        "Exito",
                        "Comentario agregado correctamente."
                    )
                    comment_window.destroy()
                    refresh_comments()
                else:
                    messagebox.showerror(
                        "Error",
                        "No se pudo agregar el comentario."
                    )

            tk.Button(
                comment_window,
                text="Guardar comentario",
                command=save_comment
            ).pack(pady=10)

        def edit_comment():
            selected = comment_list.curselection()

            if not selected:
                messagebox.showwarning(
                    "Aviso",
                    "Selecciona un comentario."
                )
                return

            comment = comments[selected[0]]

            comment_window = tk.Toplevel(window)
            comment_window.title("Modificar comentario")
            comment_window.geometry("400x300")

            tk.Label(
                comment_window,
                text="Modifica tu comentario:"
            ).pack(pady=10)

            content_text = tk.Text(
                comment_window,
                width=42,
                height=9
            )
            content_text.pack(padx=10, pady=5)
            content_text.insert("1.0", comment["content"])

            def save_changes():
                content = content_text.get(
                    "1.0", tk.END
                ).strip()

                if not content:
                    messagebox.showwarning(
                        "Datos incompletos",
                        "El comentario no puede estar vacio."
                    )
                    return

                success = update_comment(
                    comment["id"],
                    content,
                    self.user["email"],
                    self.user["role"]
                )

                if success:
                    messagebox.showinfo(
                        "Exito",
                        "Comentario actualizado."
                    )
                    comment_window.destroy()
                    refresh_comments()
                else:
                    messagebox.showerror(
                        "Error",
                        "No tienes permiso para modificar este comentario."
                    )

            tk.Button(
                comment_window,
                text="Guardar cambios",
                command=save_changes
            ).pack(pady=10)

        def remove_comment():
            selected = comment_list.curselection()

            if not selected:
                messagebox.showwarning(
                    "Aviso",
                    "Selecciona un comentario."
                )
                return

            comment = comments[selected[0]]

            confirm = messagebox.askyesno(
                "Confirmar",
                "¿Deseas eliminar este comentario?"
            )

            if not confirm:
                return

            success = delete_comment(
                comment["id"],
                self.user["email"],
                self.user["role"]
            )

            if success:
                messagebox.showinfo(
                    "Exito",
                    "Comentario eliminado."
                )
                refresh_comments()
            else:
                messagebox.showerror(
                    "Error",
                    "No tienes permiso para eliminar este comentario."
                )

        tk.Button(
            window,
            text="Agregar comentario",
            command=add_comment
        ).pack(pady=3)

        tk.Button(
            window,
            text="Modificar comentario",
            command=edit_comment
        ).pack(pady=3)

        tk.Button(
            window,
            text="Eliminar comentario",
            command=remove_comment
        ).pack(pady=3)

        refresh_comments()

    def show_comments_for_article(self, article):
        self.article_list.selection_clear(0, tk.END)

        for index, item in enumerate(self.articles):
            if item["id"] == article["id"]:
                self.article_list.selection_set(index)
                break

        self.show_comments()

    # ETIQUETAS Y CATEGORIAS

    def manage_tags_categories(self):
        selection = self.article_list.curselection()

        if not selection:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un articulo."
            )
            return

        article = self.articles[selection[0]]
        is_admin = self.user["role"] == "admin"

        window = tk.Toplevel(self.root)
        window.title("Etiquetas y categorias")
        window.geometry("750x450")

        tk.Label(
            window,
            text=f"Administrar: {article['title']}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        container = tk.Frame(window)
        container.pack(fill="both", expand=True, padx=15, pady=10)

        # SECCION DE ETIQUETAS

        tag_frame = tk.LabelFrame(
            container,
            text="Etiquetas",
            padx=10,
            pady=10
        )
        tag_frame.pack(side="left", fill="both", expand=True, padx=5)

        tag_list = tk.Listbox(tag_frame, height=12)
        tag_list.pack(fill="both", expand=True, pady=5)

        # SECCION DE CATEGORIAS

        category_frame = tk.LabelFrame(
            container,
            text="Categorias",
            padx=10,
            pady=10
        )
        category_frame.pack(side="right", fill="both", expand=True, padx=5)

        category_list = tk.Listbox(category_frame, height=12)
        category_list.pack(fill="both", expand=True, pady=5)

        def refresh_lists():
            tag_list.delete(0, tk.END)
            category_list.delete(0, tk.END)

            tags = get_tags(article["id"])
            categories = get_categories(article["id"])

            for tag in tags:
                tag_list.insert(tk.END, tag["name"])

            for category in categories:
                category_list.insert(tk.END, category["name"])

        # FUNCIONES GENERALES

        def add_item(item_type):
            name = simpledialog.askstring(
                "Agregar",
                f"Nombre de la {item_type}:",
                parent=window
            )

            if not name or not name.strip():
                return

            url = simpledialog.askstring(
                "Agregar",
                f"URL de la {item_type}:",
                parent=window
            )

            if url is None:
                return

            if item_type == "etiqueta":
                success = create_tag(
                    article["id"], name.strip(), url.strip()
                )
            else:
                success = create_category(
                    article["id"], name.strip(), url.strip()
                )

            if success:
                messagebox.showinfo(
                    "Exito",
                    f"{item_type.capitalize()} agregada correctamente."
                )
                refresh_lists()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo agregar la {item_type}."
                )

        def edit_item(item_type):
            if not is_admin:
                return

            if item_type == "etiqueta":
                selected = tag_list.curselection()
                items = get_tags(article["id"])
                update_function = update_tag
            else:
                selected = category_list.curselection()
                items = get_categories(article["id"])
                update_function = update_category

            if not selected:
                messagebox.showwarning(
                    "Aviso",
                    f"Selecciona una {item_type}."
                )
                return

            item = items[selected[0]]

            new_name = simpledialog.askstring(
                "Modificar",
                "Nuevo nombre:",
                initialvalue=item["name"],
                parent=window
            )

            if not new_name or not new_name.strip():
                return

            new_url = simpledialog.askstring(
                "Modificar",
                "Nueva URL:",
                initialvalue=item["url"],
                parent=window
            )

            if new_url is None:
                return

            success = update_function(
                item["name"],
                new_name.strip(),
                new_url.strip(),
                self.user["role"]
            )

            if success:
                messagebox.showinfo(
                    "Exito",
                    f"{item_type.capitalize()} actualizada."
                )
                refresh_lists()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo modificar la {item_type}."
                )

        def remove_item(item_type):
            if not is_admin:
                return

            if item_type == "etiqueta":
                selected = tag_list.curselection()
                items = get_tags(article["id"])
                delete_function = delete_tag
            else:
                selected = category_list.curselection()
                items = get_categories(article["id"])
                delete_function = delete_category

            if not selected:
                messagebox.showwarning(
                    "Aviso",
                    f"Selecciona una {item_type}."
                )
                return

            item = items[selected[0]]

            confirm = messagebox.askyesno(
                "Confirmar",
                f"¿Deseas eliminar la {item_type} '{item['name']}'?"
            )

            if not confirm:
                return

            success = delete_function(
                item["name"],
                self.user["role"]
            )

            if success:
                messagebox.showinfo(
                    "Exito",
                    f"{item_type.capitalize()} eliminada."
                )
                refresh_lists()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar la {item_type}."
                )

        # BOTONES DE ETIQUETAS

        tk.Button(
            tag_frame,
            text="Agregar etiqueta",
            command=lambda: add_item("etiqueta")
        ).pack(fill="x", pady=3)

        if is_admin:
            tk.Button(
                tag_frame,
                text="Modificar etiqueta",
                command=lambda: edit_item("etiqueta")
            ).pack(fill="x", pady=3)

            tk.Button(
                tag_frame,
                text="Eliminar etiqueta",
                command=lambda: remove_item("etiqueta")
            ).pack(fill="x", pady=3)

        # BOTONES DE CATEGORIAS

        tk.Button(
            category_frame,
            text="Agregar categoria",
            command=lambda: add_item("categoria")
        ).pack(fill="x", pady=3)

        if is_admin:
            tk.Button(
                category_frame,
                text="Modificar categoria",
                command=lambda: edit_item("categoria")
            ).pack(fill="x", pady=3)

            tk.Button(
                category_frame,
                text="Eliminar categoria",
                command=lambda: remove_item("categoria")
            ).pack(fill="x", pady=3)

        refresh_lists()

    # CERRAR SESION

    def logout(self):
        self.user = None
        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = BlogApp(root)
    root.mainloop()