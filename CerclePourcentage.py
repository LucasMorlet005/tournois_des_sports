import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CerclePourcentage(ctk.CTkFrame):
    def __init__(self, master, pourcentage=79.2, **kwargs):
        if 'corner_radius' not in kwargs:
            kwargs['corner_radius'] = 20
            
        super().__init__(master, fg_color="#1a1a1a", **kwargs)

        # Création de la figure Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(2.2, 2.2), dpi=100)
        self.fig.patch.set_facecolor('none')
        self.ax.set_facecolor('none')
        
        reste = 100.0 - pourcentage
        tailles = [pourcentage, reste]
        couleurs = ['#39ff14', '#ff0055'] # Vert néon et Rose/Rouge néon
        
        # Dessin de l'anneau
        self.ax.pie(
            tailles, 
            startangle=90, 
            counterclock=False, 
            colors=couleurs, 
            wedgeprops=dict(width=0.2, edgecolor='white', linewidth=2)
        )
        
        # Affichage du pourcentage au centre
        self.ax.text(
            0, 0, f"{pourcentage:.1f}%", 
            ha='center', va='center', 
            fontsize=18, fontweight='bold', 
            color='white'
        )
        
        self.ax.set(aspect="equal")

        # Intégration du canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(bg="#1a1a1a") 
        canvas_widget.pack(fill="both", expand=True, padx=15, pady=15)

    def destroy(self):
        """Nettoie et détruit proprement le canvas et la figure Matplotlib avant la fermeture."""
        try:
            if hasattr(self, 'canvas') and self.canvas:
                # Détruit le widget du canvas pour stopper les tâches de fond (DPI)
                self.canvas.get_tk_widget().destroy()
        except Exception:
            pass
            
        try:
            if hasattr(self, 'fig') and self.fig:
                # Ferme la figure Matplotlib
                plt.close(self.fig)
        except Exception:
            pass
            
        super().destroy()